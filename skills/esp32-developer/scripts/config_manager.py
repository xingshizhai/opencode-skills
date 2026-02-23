#!/usr/bin/env python3
"""
ESP32 Developer Configuration Manager

This module handles ESP-IDF installation detection, version selection,
and user configuration for the esp32-developer skill.
"""

import os
import sys
import json
import re
import glob
import subprocess
from pathlib import Path

CONFIG_FILE = os.path.expanduser("~/.esp32-developer-config.json")
DEFAULT_CONFIG = {
    "idf_path": "",
    "idf_version": "",
    "default_target": "esp32",
    "default_port": "",
    "default_baud": 460800
}

# Common ESP-IDF installation locations
COMMON_IDF_PATHS = [
    os.path.expanduser("~/esp/esp-idf"),
    os.path.expanduser("~/esp-idf"),
    "/opt/esp-idf",
    "/usr/local/esp-idf",
]

# Supported ESP32 targets
SUPPORTED_TARGETS = [
    "esp32",
    "esp32s2",
    "esp32s3",
    "esp32c2",
    "esp32c3",
    "esp32c6",
    "esp32h2",
]

def detect_idf_installations():
    """
    Detect ESP-IDF installations in common locations.
    
    Returns:
        list: List of tuples (path, version) for found installations
    """
    installations = []
    
    # Check IDF_PATH environment variable first
    idf_path = os.environ.get('IDF_PATH')
    if idf_path and os.path.exists(idf_path):
        version = get_idf_version(idf_path)
        installations.append((idf_path, version or "unknown"))
    
    # Check common installation paths
    for path in COMMON_IDF_PATHS:
        if os.path.exists(path):
            # Check if it looks like ESP-IDF (has version.txt or export.sh)
            version_file = os.path.join(path, "version.txt")
            export_script = os.path.join(path, "export.sh")
            
            if os.path.exists(export_script):
                version = get_idf_version(path)
                installations.append((path, version or "unknown"))
    
    # Remove duplicates
    unique_installations = []
    seen_paths = set()
    for path, version in installations:
        if path not in seen_paths:
            seen_paths.add(path)
            unique_installations.append((path, version))
    
    return unique_installations

def get_idf_version(idf_path):
    """
    Get ESP-IDF version from installation.
    
    Args:
        idf_path: Path to ESP-IDF installation
    
    Returns:
        str: Version string or None if not found
    """
    # Try version.txt first
    version_file = os.path.join(idf_path, "version.txt")
    if os.path.exists(version_file):
        try:
            with open(version_file, 'r') as f:
                content = f.read().strip()
                # Extract version number
                match = re.search(r'v(\d+\.\d+\.\d+)', content)
                if match:
                    return f"v{match.group(1)}"
                return content
        except:
            pass
    
    # Try git describe
    git_dir = os.path.join(idf_path, ".git")
    if os.path.exists(git_dir):
        try:
            result = subprocess.run(
                ["git", "describe", "--tags"],
                cwd=idf_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
    
    # Try CMakeLists.txt
    cmake_file = os.path.join(idf_path, "CMakeLists.txt")
    if os.path.exists(cmake_file):
        try:
            with open(cmake_file, 'r') as f:
                content = f.read()
                # Look for version in CMakeLists.txt
                match = re.search(r'set\(IDF_VERSION_MAJOR\s+(\d+)\)', content)
                if match:
                    major = match.group(1)
                    minor_match = re.search(r'set\(IDF_VERSION_MINOR\s+(\d+)\)', content)
                    patch_match = re.search(r'set\(IDF_VERSION_PATCH\s+(\d+)\)', content)
                    minor = minor_match.group(1) if minor_match else "0"
                    patch = patch_match.group(1) if patch_match else "0"
                    return f"v{major}.{minor}.{patch}"
        except:
            pass
    
    return None

def load_config():
    """
    Load user configuration from config file.
    
    Returns:
        dict: Configuration dictionary
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Ensure all default keys are present
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except json.JSONDecodeError:
            print(f"Warning: Config file {CONFIG_FILE} is corrupted. Using defaults.")
    
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """
    Save user configuration to config file.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        bool: True if successful
    """
    try:
        # Ensure directory exists
        config_dir = os.path.dirname(CONFIG_FILE)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def interactive_setup():
    """
    Interactive setup wizard for ESP-IDF configuration.
    
    Returns:
        dict: Updated configuration
    """
    print("=" * 60)
    print("ESP32 Developer Configuration Setup")
    print("=" * 60)
    
    config = load_config()
    
    # Step 1: Detect ESP-IDF installations
    print("\n1. ESP-IDF Installation Detection")
    print("-" * 40)
    
    installations = detect_idf_installations()
    
    if not installations:
        print("No ESP-IDF installations found automatically.")
        print("Please specify your ESP-IDF installation path.")
        
        while True:
            idf_path = input("ESP-IDF path: ").strip()
            if not idf_path:
                print("Installation cancelled.")
                return None
            
            if os.path.exists(idf_path):
                version = get_idf_version(idf_path)
                if version:
                    print(f"Found ESP-IDF {version} at {idf_path}")
                    config["idf_path"] = idf_path
                    config["idf_version"] = version
                    break
                else:
                    print("Path exists but doesn't appear to be ESP-IDF.")
                    print("Please check the path and try again.")
            else:
                print("Path does not exist. Please try again.")
    else:
        print("Found the following ESP-IDF installations:")
        for i, (path, version) in enumerate(installations, 1):
            print(f"  {i}. {path} ({version})")
        
        print(f"  {len(installations) + 1}. Specify custom path")
        
        while True:
            try:
                choice = input(f"\nSelect installation [1-{len(installations) + 1}]: ").strip()
                if not choice:
                    print("Installation cancelled.")
                    return None
                
                choice_idx = int(choice)
                
                if 1 <= choice_idx <= len(installations):
                    selected_path, selected_version = installations[choice_idx - 1]
                    config["idf_path"] = selected_path
                    config["idf_version"] = selected_version
                    print(f"Selected: {selected_path} ({selected_version})")
                    break
                elif choice_idx == len(installations) + 1:
                    custom_path = input("Custom ESP-IDF path: ").strip()
                    if os.path.exists(custom_path):
                        version = get_idf_version(custom_path)
                        if version:
                            config["idf_path"] = custom_path
                            config["idf_version"] = version
                            print(f"Selected: {custom_path} ({version})")
                            break
                        else:
                            print("Path exists but doesn't appear to be ESP-IDF.")
                    else:
                        print("Path does not exist.")
                else:
                    print(f"Please enter a number between 1 and {len(installations) + 1}")
            except ValueError:
                print("Please enter a valid number.")
    
    # Step 2: Default target selection
    print("\n2. Default ESP32 Target")
    print("-" * 40)
    print("Available targets:")
    for i, target in enumerate(SUPPORTED_TARGETS, 1):
        print(f"  {i}. {target}")
    
    while True:
        target_choice = input(f"\nSelect default target [1-{len(SUPPORTED_TARGETS)}] (default: 1 for esp32): ").strip()
        
        if not target_choice:
            config["default_target"] = "esp32"
            print("Default target set to: esp32")
            break
        
        try:
            target_idx = int(target_choice)
            if 1 <= target_idx <= len(SUPPORTED_TARGETS):
                config["default_target"] = SUPPORTED_TARGETS[target_idx - 1]
                print(f"Default target set to: {config['default_target']}")
                break
            else:
                print(f"Please enter a number between 1 and {len(SUPPORTED_TARGETS)}")
        except ValueError:
            print("Please enter a valid number.")
    
    # Step 3: Default serial port (optional)
    print("\n3. Default Serial Port (Optional)")
    print("-" * 40)
    print("You can specify a default serial port for flashing and monitoring.")
    print("Leave blank to auto-detect each time.")
    
    default_port = input("Default serial port (e.g., /dev/ttyUSB0, COM3): ").strip()
    if default_port:
        config["default_port"] = default_port
        print(f"Default port set to: {default_port}")
    
    # Step 4: Save configuration
    print("\n4. Saving Configuration")
    print("-" * 40)
    
    if save_config(config):
        print(f"Configuration saved to: {CONFIG_FILE}")
        print("\nSummary:")
        print(f"  ESP-IDF: {config['idf_path']} ({config['idf_version']})")
        print(f"  Default target: {config['default_target']}")
        if config['default_port']:
            print(f"  Default port: {config['default_port']}")
        
        # Update environment
        os.environ['IDF_PATH'] = config['idf_path']
        print(f"\nIDF_PATH environment variable set to: {config['idf_path']}")
        print("\nYou can update this configuration anytime by running:")
        print("  python scripts/config_manager.py --setup")
        
        return config
    else:
        print("Failed to save configuration.")
        return None

def get_configured_idf_path():
    """
    Get configured IDF_PATH with fallback logic.
    
    Returns:
        str: IDF_PATH or None if not configured
    """
    # 1. Check environment variable
    idf_path = os.environ.get('IDF_PATH')
    if idf_path and os.path.exists(idf_path):
        return idf_path
    
    # 2. Check config file
    config = load_config()
    if config.get('idf_path') and os.path.exists(config['idf_path']):
        # Set environment variable for child processes
        os.environ['IDF_PATH'] = config['idf_path']
        return config['idf_path']
    
    # 3. Try to detect
    installations = detect_idf_installations()
    if installations:
        # Use the first one found
        idf_path, _ = installations[0]
        os.environ['IDF_PATH'] = idf_path
        return idf_path
    
    return None

def ensure_configured():
    """
    Ensure ESP-IDF is configured, prompt if not.
    
    Returns:
        dict: Configuration or None if setup cancelled
    """
    config = load_config()
    
    # Check if we have a valid IDF_PATH
    idf_path = get_configured_idf_path()
    if not idf_path:
        print("ESP-IDF is not configured.")
        print("Please run the setup wizard.")
        return interactive_setup()
    
    # Update config with current IDF_PATH if different
    if config.get('idf_path') != idf_path:
        config['idf_path'] = idf_path
        config['idf_version'] = get_idf_version(idf_path) or "unknown"
        save_config(config)
    
    return config

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ESP32 Developer Configuration Manager")
    parser.add_argument("--setup", action="store_true", help="Run interactive setup wizard")
    parser.add_argument("--show", action="store_true", help="Show current configuration")
    parser.add_argument("--reset", action="store_true", help="Reset configuration to defaults")
    parser.add_argument("--path", action="store_true", help="Show IDF_PATH only")
    
    args = parser.parse_args()
    
    if args.setup:
        interactive_setup()
    elif args.show:
        config = load_config()
        print("Current Configuration:")
        print(json.dumps(config, indent=2))
    elif args.reset:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            print("Configuration reset to defaults.")
        else:
            print("No configuration file found.")
    elif args.path:
        idf_path = get_configured_idf_path()
        if idf_path:
            print(idf_path)
        else:
            print("IDF_PATH not configured", file=sys.stderr)
            sys.exit(1)
    else:
        # Default: show config
        config = load_config()
        print("ESP32 Developer Configuration")
        print("=" * 40)
        print(f"Config file: {CONFIG_FILE}")
        print(f"ESP-IDF: {config.get('idf_path', 'Not configured')}")
        if config.get('idf_path'):
            print(f"Version: {config.get('idf_version', 'unknown')}")
        print(f"Default target: {config.get('default_target', 'esp32')}")
        print(f"Default port: {config.get('default_port', 'auto-detect')}")
        print("\nCommands:")
        print("  --setup   Run interactive setup")
        print("  --show    Show detailed configuration")
        print("  --reset   Reset to defaults")
        print("  --path    Show IDF_PATH only")

if __name__ == "__main__":
    main()