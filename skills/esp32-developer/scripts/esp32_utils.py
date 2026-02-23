#!/usr/bin/env python3
"""
ESP32 Developer Utilities

Shared utilities for ESP32 development scripts.
"""

import os
import sys
import subprocess
import re
import glob
import json
import time
from pathlib import Path

# Import config_manager for configuration
import config_manager

CONFIG_FILE = os.path.expanduser("~/.esp32-developer-config.json")

def setup_esp_idf_environment():
    """
    Setup ESP-IDF environment by sourcing export.sh or setting environment variables.
    Returns True if successful, False otherwise.
    """
    # First, get configured IDF_PATH
    idf_path = config_manager.get_configured_idf_path()
    if not idf_path:
        print("ERROR: ESP-IDF is not configured.")
        print("Please run: python scripts/config_manager.py --setup")
        return False
    
    # Check if IDF_PATH exists
    if not os.path.exists(idf_path):
        print(f"ERROR: IDF_PATH directory does not exist: {idf_path}")
        print("Please reconfigure ESP-IDF: python scripts/config_manager.py --setup")
        return False
    
    # Set IDF_PATH environment variable
    os.environ['IDF_PATH'] = idf_path
    
    # Try to source export.sh to setup environment
    export_script = os.path.join(idf_path, "export.sh")
    
    if os.path.exists(export_script):
        try:
            # Use a subprocess to source export.sh and capture environment
            env_cmd = f"source {export_script} > /dev/null 2>&1 && python3 -c \"import os; import json; print(json.dumps(dict(os.environ)))\""
            
            result = subprocess.run(
                ["bash", "-c", env_cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    # Update environment with sourced variables
                    env_dict = json.loads(result.stdout)
                    for key, value in env_dict.items():
                        # Update environment variables, preferring sourced ones
                        os.environ[key] = value
                except json.JSONDecodeError:
                    # If we can't parse JSON, just set PATH for idf.py
                    pass
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            # Fall back to setting PATH manually
            pass
    
    # Check if idf.py is now available
    try:
        result = subprocess.run(['idf.py', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_match = re.search(r'ESP-IDF v(\d+\.\d+\.\d+)', result.stdout)
            if version_match:
                print(f"✅ ESP-IDF {version_match.group(1)} environment ready")
            else:
                print("✅ ESP-IDF environment ready")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # If idf.py not found, try to find it in common locations
    possible_idf_py_paths = [
        os.path.join(idf_path, "tools", "idf.py"),
        os.path.join(idf_path, "idf.py"),
        os.path.join(os.path.dirname(idf_path), "tools", "idf.py")
    ]
    
    for idf_py_path in possible_idf_py_paths:
        if os.path.exists(idf_py_path):
            # Add to PATH
            idf_py_dir = os.path.dirname(idf_py_path)
            if idf_py_dir not in os.environ.get('PATH', '').split(':'):
                os.environ['PATH'] = idf_py_dir + ':' + os.environ.get('PATH', '')
            
            # Check again
            try:
                subprocess.run(['idf.py', '--version'], capture_output=True, check=True)
                print(f"✅ ESP-IDF environment ready (idf.py found at {idf_py_path})")
                return True
            except:
                pass
    
    print("ERROR: idf.py command not found.")
    print("Please make sure ESP-IDF environment is properly sourced.")
    print(f"IDF_PATH is set to: {idf_path}")
    print("\nTry running manually: source $IDF_PATH/export.sh")
    print("\nOr add ESP-IDF tools to your PATH.")
    return False

def get_project_info(project_path=None):
    """
    Get information about an ESP32 project.
    Returns dict with project info or None if not a valid project.
    """
    if not project_path:
        project_path = os.getcwd()
    
    project_info = {
        'path': project_path,
        'is_valid': False,
        'has_build': False,
        'build_dir': None,
        'binary_files': []
    }
    
    # Check if it's an ESP-IDF project
    cmake_file = os.path.join(project_path, "CMakeLists.txt")
    if os.path.exists(cmake_file):
        project_info['is_valid'] = True
        
        # Check for build directory
        build_dir = os.path.join(project_path, "build")
        if os.path.exists(build_dir):
            project_info['has_build'] = True
            project_info['build_dir'] = build_dir
            
            # Look for binaries
            bin_dir = os.path.join(build_dir, "bin")
            if os.path.exists(bin_dir):
                for f in os.listdir(bin_dir):
                    if f.endswith('.bin') or f.endswith('.elf'):
                        project_info['binary_files'].append(os.path.join(bin_dir, f))
    
    return project_info

def detect_serial_ports():
    """
    Detect available serial ports.
    Returns list of port paths.
    """
    ports = []
    
    # Platform-specific detection
    if sys.platform.startswith('linux'):
        # Linux
        possible_ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyS*")
        for port in possible_ports:
            if os.path.exists(port):
                ports.append(port)
    
    elif sys.platform.startswith('darwin'):
        # macOS
        possible_ports = glob.glob("/dev/cu.usbserial*") + glob.glob("/dev/cu.usbmodem*")
        for port in possible_ports:
            if os.path.exists(port):
                ports.append(port)
    
    elif sys.platform.startswith('win'):
        # Windows
        for i in range(256):
            port = f"COM{i}"
            # Check if port exists by trying to open it
            try:
                import serial
                ser = serial.Serial(port)
                ser.close()
                ports.append(port)
            except:
                pass
    
    return ports

def run_idf_command(args, project_path=None, capture_output=True, timeout=300):
    """
    Run an idf.py command with proper environment setup.
    Returns subprocess.CompletedProcess object.
    """
    # Ensure environment is set up
    if not setup_esp_idf_environment():
        raise RuntimeError("Failed to setup ESP-IDF environment")
    
    # Change to project directory if specified
    original_dir = None
    if project_path and os.path.exists(project_path):
        original_dir = os.getcwd()
        os.chdir(project_path)
    
    try:
        cmd = ['idf.py'] + args
        
        print(f"Running: {' '.join(cmd)}")
        if project_path:
            print(f"In directory: {project_path}")
        
        start_time = time.time()
        
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Command completed successfully ({elapsed_time:.1f}s)")
        else:
            print(f"❌ Command failed with code {result.returncode} ({elapsed_time:.1f}s)")
        
        return result
        
    finally:
        # Restore original directory
        if original_dir:
            os.chdir(original_dir)

def get_default_target():
    """Get default target from config."""
    config = config_manager.load_config()
    return config.get('default_target', 'esp32')

def get_default_port():
    """Get default port from config, or auto-detect."""
    config = config_manager.load_config()
    default_port = config.get('default_port', '')
    
    if default_port and os.path.exists(default_port):
        return default_port
    
    # Auto-detect
    ports = detect_serial_ports()
    if ports:
        return ports[0]
    
    return None

def is_esp32_project(project_path):
    """Check if directory is an ESP32 project."""
    cmake_file = os.path.join(project_path, "CMakeLists.txt")
    if not os.path.exists(cmake_file):
        return False
    
    # Check if it contains ESP-IDF specific content
    try:
        with open(cmake_file, 'r') as f:
            content = f.read()
            # Look for ESP-IDF specific patterns
            if 'idf_component_register' in content or 'include($ENV{IDF_PATH}/tools/cmake/project.cmake)' in content:
                return True
    except:
        pass
    
    return False

def format_size(bytes_size):
    """Format bytes size to human readable string."""
    for unit in ['B', 'KB', 'MB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}GB"

def print_progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    """
    Print progress bar.
    """
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    
    # Print new line on completion
    if iteration == total:
        print()