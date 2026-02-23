#!/usr/bin/env python3
"""
Flash ESP32 firmware to a development board.

Enhanced version with better port detection, error handling, and user feedback.

Usage:
    flash_esp32.py [--port SERIAL_PORT] [--baud BAUD_RATE] [--path PROJECT_PATH] 
                   [--monitor] [--setup] [--verbose] [--no-reset]

Examples:
    flash_esp32.py
    flash_esp32.py --port /dev/ttyUSB0 --baud 460800
    flash_esp32.py --port COM3 --baud 115200 --monitor
    flash_esp32.py --setup  # Run setup wizard first
    flash_esp32.py --verbose --no-reset  # Verbose output, don't reset board
"""

import os
import sys
import subprocess
import argparse
import time

# Add config manager to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config_manager
import esp32_utils

def check_esp_idf(setup_if_needed=True, verbose=False):
    """Check if ESP-IDF environment is set up."""
    # Try to get configured IDF_PATH
    idf_path = config_manager.get_configured_idf_path()
    
    if not idf_path:
        if setup_if_needed:
            print("⚠️  ESP-IDF is not configured.")
            print("Run setup wizard: python scripts/config_manager.py --setup")
        return False
    
    if not os.path.exists(idf_path):
        print(f"❌ IDF_PATH directory does not exist: {idf_path}")
        print("Please reconfigure ESP-IDF: python scripts/config_manager.py --setup")
        return False
    
    # Use esp32_utils to setup environment
    if verbose:
        print(f"🔧 Setting up ESP-IDF environment from: {idf_path}")
    
    return esp32_utils.setup_esp_idf_environment()

def flash_project(project_path, port, baud, monitor, verbose, no_reset, setup_if_needed=True):
    """Flash the ESP32 project."""
    # Load configuration for default port
    config = config_manager.load_config()
    
    # Use default port from config if not specified
    if not port:
        port = esp32_utils.get_default_port()
        if port:
            print(f"🔌 Using detected port: {port}")
    
    # Determine project directory
    if not project_path:
        project_path = os.getcwd()
    
    if not os.path.exists(project_path):
        print(f"❌ Project path does not exist: {project_path}")
        return False
    
    # Check if project is built
    project_info = esp32_utils.get_project_info(project_path)
    if not project_info['has_build']:
        print(f"❌ Project not built. Build the project first.")
        print(f"   Run: idf.py build")
        print(f"   Or: python scripts/build_esp32_project.py --path {project_path}")
        return False
    
    # Check for serial port
    if not port:
        # Try to detect ports
        ports = esp32_utils.detect_serial_ports()
        if ports:
            print(f"🔍 Detected serial ports:")
            for p in ports:
                print(f"   • {p}")
            port = ports[0]
            print(f"🔌 Using first detected port: {port}")
        else:
            print("❌ No serial port detected.")
            print("\n💡 Troubleshooting tips:")
            print("   1. Check USB cable connection")
            print("   2. Ensure board is powered")
            print("   3. Check if drivers are installed")
            print("   4. Try specifying port manually with --port")
            print("\nCommon ports:")
            print("   Linux: /dev/ttyUSB0, /dev/ttyACM0")
            print("   Windows: COM3, COM4")
            print("   macOS: /dev/cu.usbserial-*")
            return False
    
    print(f"\n⚡ Flashing ESP32 project at {project_path}")
    print(f"   Port: {port}")
    print(f"   Baud rate: {baud}")
    if verbose:
        print(f"   Project has build: {project_info['has_build']}")
        print(f"   Binary files: {len(project_info['binary_files'])}")
    
    try:
        # Build flash command
        cmd = ['-p', port, '-b', str(baud), 'flash']
        
        if no_reset:
            cmd.extend(['--before', 'no_reset', '--after', 'no_reset'])
        
        if monitor:
            cmd.append('monitor')
            print("   📺 Starting monitor after flash...")
        
        print("   🔥 Flashing firmware...")
        if not no_reset:
            print("   💡 Tip: Press BOOT button if flashing doesn't start")
        
        # Run flash command
        result = esp32_utils.run_idf_command(cmd, project_path, capture_output=not verbose)
        
        if result.returncode == 0:
            print("\n✅ Flash successful!")
            
            if monitor:
                print("   📺 Monitor is running. Press Ctrl+] to exit monitor.")
            else:
                print(f"\n📡 To start serial monitor:")
                print(f"   idf.py -p {port} monitor")
                print(f"   or: python scripts/monitor_serial.py --port {port}")
            
            # Show quick verification
            print(f"\n🔍 To verify flash:")
            print(f"   1. Check board LEDs (usually power LED should be on)")
            print(f"   2. Monitor serial output for application logs")
            print(f"   3. Check if application functions as expected")
            
            return True
        else:
            print(f"\n❌ Flash failed!")
            
            if not verbose and result.stderr:
                print(f"\n🔍 Error summary:")
                error_lines = result.stderr.split('\n')
                error_shown = 0
                for line in error_lines:
                    if 'error' in line.lower() or 'failed' in line.lower():
                        print(f"   {line}")
                        error_shown += 1
                        if error_shown >= 5:
                            break
            
            print(f"\n💡 Troubleshooting tips:")
            print(f"   1. Check cable connection and power")
            print(f"   2. Press BOOT button while flashing (if no auto-reset)")
            print(f"   3. Try different baud rate: --baud 115200")
            print(f"   4. Check if correct port is selected")
            print(f"   5. Try --no-reset option if board doesn't reset properly")
            print(f"   6. Run with --verbose for detailed output")
            
            return False
            
    except Exception as e:
        print(f"❌ Flash failed with exception: {e}")
        import traceback
        if verbose:
            traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description="Flash ESP32 firmware to a development board")
    parser.add_argument("--port", help="Serial port (e.g., /dev/ttyUSB0, COM3). If not specified, auto-detects.")
    parser.add_argument("--baud", type=int, default=460800, help="Baud rate (default: 460800)")
    parser.add_argument("--path", help="Path to project directory (default: current directory)")
    parser.add_argument("--monitor", action="store_true", help="Start serial monitor after flashing")
    parser.add_argument("--setup", action="store_true", help="Run setup wizard before flashing")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument("--no-reset", action="store_true", help="Don't reset board before/after flash")
    
    args = parser.parse_args()
    
    # Run setup wizard if requested
    setup_if_needed = True
    if args.setup:
        print("🔧 Running ESP-IDF setup wizard...")
        config = config_manager.interactive_setup()
        if not config:
            print("❌ Setup cancelled.")
            sys.exit(1)
        setup_if_needed = False  # Already setup
        print("✅ Setup complete")
    
    # Check ESP-IDF environment
    if not check_esp_idf(setup_if_needed, args.verbose):
        if setup_if_needed and not args.setup:
            print("\n💡 Run with --setup to configure ESP-IDF")
        sys.exit(1)
    
    # Flash project
    success = flash_project(
        args.path, 
        args.port, 
        args.baud, 
        args.monitor, 
        args.verbose,
        args.no_reset,
        setup_if_needed
    )
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()