#!/usr/bin/env python3
"""
Monitor ESP32 serial output and analyze logs.

Enhanced version with pyserial support for non-interactive environments,
better filtering, and logging capabilities.

Usage:
    monitor_serial.py [--port SERIAL_PORT] [--baud BAUD_RATE] [--path PROJECT_PATH] 
                      [--filter FILTER] [--save LOG_FILE] [--no-color] [--setup]
                      [--method {idf,pyserial}] [--timeout SECONDS] [--exit-on ERROR_PATTERN]

Examples:
    monitor_serial.py
    monitor_serial.py --port /dev/ttyUSB0 --baud 115200
    monitor_serial.py --filter "error|warn" --save debug.log
    monitor_serial.py --setup  # Run setup wizard first
    monitor_serial.py --method pyserial  # Use pyserial instead of idf.py monitor
    monitor_serial.py --timeout 30 --exit-on "panic"  # Exit after 30s or on panic
"""

import os
import sys
import subprocess
import argparse
import re
import signal
import time
import serial
import serial.tools.list_ports

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
    
    # Use esp32_utils to setup environment (only needed for idf.py method)
    if verbose:
        print(f"🔧 Setting up ESP-IDF environment from: {idf_path}")
    
    # Note: For pyserial method, we don't need full ESP-IDF environment
    return True

def monitor_with_idf(port, baud, project_path, filter_pattern, log_file, no_color):
    """Monitor using idf.py monitor command."""
    print(f"📺 Starting monitor with idf.py...")
    
    # Build monitor command
    cmd = ['-p', port, '-b', str(baud), 'monitor']
    
    if no_color:
        cmd.extend(['--color', 'no'])
    
    try:
        result = esp32_utils.run_idf_command(cmd, project_path, capture_output=False, timeout=None)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ idf.py monitor failed: {e}")
        return False

def monitor_with_pyserial(port, baud, filter_pattern, log_file, exit_on_pattern, timeout):
    """Monitor using pyserial library (works in non-interactive environments)."""
    print(f"📡 Starting monitor with pyserial...")
    print(f"   Port: {port}")
    print(f"   Baud: {baud}")
    print(f"   Timeout: {timeout}s" if timeout else "   Timeout: None")
    
    if filter_pattern:
        print(f"   Filter: {filter_pattern}")
    if exit_on_pattern:
        print(f"   Exit on: {exit_on_pattern}")
    
    # Compile regex patterns
    filter_regex = None
    exit_regex = None
    
    if filter_pattern:
        try:
            filter_regex = re.compile(filter_pattern, re.IGNORECASE)
        except re.error as e:
            print(f"❌ Invalid filter pattern: {e}")
            return False
    
    if exit_on_pattern:
        try:
            exit_regex = re.compile(exit_on_pattern, re.IGNORECASE)
        except re.error as e:
            print(f"❌ Invalid exit pattern: {e}")
            return False
    
    # Open log file if specified
    log_handle = None
    if log_file:
        try:
            log_handle = open(log_file, 'w')
            print(f"   Logging to: {log_file}")
        except Exception as e:
            print(f"❌ Failed to open log file: {e}")
            return False
    
    # Open serial port
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1  # Read timeout
        )
    except serial.SerialException as e:
        print(f"❌ Failed to open serial port {port}: {e}")
        print("\n💡 Troubleshooting tips:")
        print(f"   1. Check if port exists: ls {port} (Linux/macOS)")
        print(f"   2. Check permissions: sudo chmod 666 {port} (Linux)")
        print(f"   3. Check if another program is using the port")
        print(f"   4. Try different baud rate (115200, 74880, 460800)")
        return False
    
    print("\n" + "="*60)
    print("ESP32 Serial Monitor (pyserial)")
    print("="*60)
    print("Press Ctrl+C to exit")
    print("="*60)
    print("Waiting for serial data...")
    print("="*60 + "\n")
    
    line_count = 0
    match_count = 0
    start_time = time.time()
    
    try:
        buffer = ""
        
        while True:
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                print(f"\n⏰ Timeout reached ({timeout}s)")
                break
            
            # Read from serial port
            try:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    try:
                        text = data.decode('utf-8', errors='ignore')
                        buffer += text
                        
                        # Process complete lines
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.rstrip('\r')
                            line_count += 1
                            
                            # Apply filter if specified
                            if filter_regex:
                                if filter_regex.search(line):
                                    match_count += 1
                                    print(f"[{match_count}] {line}")
                            else:
                                print(line)
                            
                            # Write to log file if specified
                            if log_handle:
                                log_handle.write(line + '\n')
                                log_handle.flush()
                            
                            # Check exit pattern
                            if exit_regex and exit_regex.search(line):
                                print(f"\n⚠️  Exit pattern matched: {exit_on_pattern}")
                                break
                    
                    except UnicodeDecodeError:
                        # Skip non-UTF8 data
                        pass
            
            except serial.SerialException as e:
                print(f"\n⚠️  Serial port error: {e}")
                break
            
            # Small delay to prevent CPU spinning
            time.sleep(0.01)
            
            # Check for KeyboardInterrupt
            if not ser.is_open:
                break
    
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped by user")
    
    finally:
        # Cleanup
        if ser.is_open:
            ser.close()
        
        if log_handle:
            log_handle.close()
            print(f"\n💾 Log saved to: {log_file}")
        
        elapsed_time = time.time() - start_time
        print(f"\n📊 Statistics:")
        print(f"   Lines processed: {line_count}")
        print(f"   Time elapsed: {elapsed_time:.1f}s")
        if filter_pattern:
            print(f"   Lines matched: {match_count}")
    
    return True

def start_monitor(project_path, port, baud, filter_pattern, log_file, no_color, 
                  method, timeout, exit_on_pattern, setup_if_needed=True):
    """Start serial monitor with optional filtering and logging."""
    # Load configuration for default port
    config = config_manager.load_config()
    
    # Use default port from config if not specified
    if not port and config.get('default_port'):
        port = config['default_port']
        print(f"🔌 Using default port from config: {port}")
    
    # Detect port if not specified (and not in config)
    if not port:
        port = esp32_utils.get_default_port()
        if port:
            print(f"🔌 Using detected port: {port}")
        else:
            print("❌ No serial port detected.")
            print("\n💡 Please specify port manually with --port")
            print("Common ports:")
            print("   Linux: /dev/ttyUSB0, /dev/ttyACM0")
            print("   Windows: COM3, COM4")
            print("   macOS: /dev/cu.usbserial-*")
            return False
    
    # Determine project directory (only needed for idf.py method)
    if not project_path:
        project_path = os.getcwd()
    
    print(f"\n🚀 Starting ESP32 serial monitor")
    print(f"   Method: {method}")
    print(f"   Port: {port}")
    print(f"   Baud rate: {baud}")
    
    if method == 'idf':
        # Setup ESP-IDF environment for idf.py method
        if not esp32_utils.setup_esp_idf_environment():
            print("❌ Failed to setup ESP-IDF environment for idf.py method")
            print("   Trying pyserial method instead...")
            method = 'pyserial'
    
    if method == 'idf':
        return monitor_with_idf(port, baud, project_path, filter_pattern, log_file, no_color)
    else:  # pyserial
        return monitor_with_pyserial(port, baud, filter_pattern, log_file, exit_on_pattern, timeout)

def main():
    parser = argparse.ArgumentParser(description="Monitor ESP32 serial output and analyze logs")
    parser.add_argument("--port", help="Serial port (e.g., /dev/ttyUSB0, COM3). If not specified, auto-detects.")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--path", help="Path to project directory (default: current directory)")
    parser.add_argument("--filter", help="Filter pattern (regex) to show only matching lines")
    parser.add_argument("--save", help="Save log to file")
    parser.add_argument("--no-color", action="store_true", help="Disable color output (idf.py method only)")
    parser.add_argument("--setup", action="store_true", help="Run setup wizard before monitoring")
    parser.add_argument("--method", choices=['idf', 'pyserial'], default='pyserial', 
                       help="Monitoring method (default: pyserial for non-interactive environments)")
    parser.add_argument("--timeout", type=int, help="Timeout in seconds (pyserial method only)")
    parser.add_argument("--exit-on", help="Exit when pattern is matched (pyserial method only)")
    
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
    
    # Check basic configuration
    if not check_esp_idf(setup_if_needed, False):
        if setup_if_needed and not args.setup:
            print("\n💡 Run with --setup to configure ESP-IDF")
        # For pyserial method, we can continue without full ESP-IDF setup
        if args.method == 'idf':
            sys.exit(1)
    
    # Start monitor
    success = start_monitor(
        args.path, 
        args.port, 
        args.baud, 
        args.filter,
        args.save,
        args.no_color,
        args.method,
        args.timeout,
        args.exit_on,
        setup_if_needed
    )
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()