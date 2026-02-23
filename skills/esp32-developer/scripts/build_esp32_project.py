#!/usr/bin/env python3
"""
Build an ESP32 project using ESP-IDF.

Enhanced version with better error handling, environment setup, and user feedback.

Usage:
    build_esp32_project.py [--path PROJECT_PATH] [--target TARGET] [--clean] [--setup] [--verbose]

Examples:
    build_esp32_project.py
    build_esp32_project.py --path /home/user/my_project --target esp32s3
    build_esp32_project.py --clean
    build_esp32_project.py --setup  # Run setup wizard first
    build_esp32_project.py --verbose  # Show detailed output
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

def build_project(project_path, target, clean, verbose, setup_if_needed=True):
    """Build the ESP32 project."""
    # Load configuration for default target
    config = config_manager.load_config()
    
    # Use default target if not specified
    if not target:
        target = config.get('default_target', 'esp32')
        print(f"🎯 Using default target: {target}")
    
    # Determine project directory
    if not project_path:
        project_path = os.getcwd()
    
    if not os.path.exists(project_path):
        print(f"❌ Project path does not exist: {project_path}")
        return False
    
    # Check if it's an ESP-IDF project
    if not esp32_utils.is_esp32_project(project_path):
        print(f"❌ Not an ESP-IDF project: {project_path}")
        print("Make sure the directory contains CMakeLists.txt with ESP-IDF configuration.")
        return False
    
    print(f"\n🔨 Building ESP32 project at {project_path}")
    print(f"   Target: {target}")
    if verbose:
        project_info = esp32_utils.get_project_info(project_path)
        print(f"   Project valid: {project_info['is_valid']}")
        print(f"   Has existing build: {project_info['has_build']}")
    
    try:
        # Clean build if requested
        if clean:
            print("   🧹 Cleaning build...")
            result = esp32_utils.run_idf_command(['fullclean'], project_path, capture_output=not verbose)
            if result.returncode != 0:
                print(f"   ❌ Clean failed")
                if not verbose and result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")
                return False
        
        # Set target if specified
        if target:
            print(f"   🎯 Setting target to {target}...")
            result = esp32_utils.run_idf_command(['set-target', target], project_path, capture_output=not verbose)
            if result.returncode != 0:
                print(f"   ❌ Set target failed")
                if not verbose and result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")
                return False
        
        # Build the project
        print("   🔧 Building project...")
        if verbose:
            print("   (Verbose output enabled)")
        
        result = esp32_utils.run_idf_command(['build'], project_path, capture_output=not verbose)
        
        if result.returncode == 0:
            print("\n✅ Build successful!")
            
            # Show build summary
            project_info = esp32_utils.get_project_info(project_path)
            if project_info['has_build'] and project_info['binary_files']:
                print(f"\n📁 Generated binaries:")
                for binary in project_info['binary_files']:
                    size = os.path.getsize(binary) if os.path.exists(binary) else 0
                    print(f"   • {os.path.basename(binary)} ({esp32_utils.format_size(size)})")
            
            # Show flash instructions
            default_port = esp32_utils.get_default_port()
            port_hint = f" -p {default_port}" if default_port else ""
            
            print(f"\n⚡ To flash the firmware:")
            print(f"   idf.py{port_hint} flash")
            print(f"   or: python scripts/flash_esp32.py{port_hint}")
            
            if default_port:
                print(f"\n📡 Detected serial port: {default_port}")
            
            return True
        else:
            print(f"\n❌ Build failed!")
            
            if not verbose and result.stderr:
                print(f"\n🔍 Error summary:")
                error_lines = result.stderr.split('\n')
                for line in error_lines[-10:]:  # Show last 10 error lines
                    if line.strip():
                        print(f"   {line}")
            
            print(f"\n💡 Troubleshooting tips:")
            print(f"   1. Check CMakeLists.txt for errors")
            print(f"   2. Run with --clean to clean build")
            print(f"   3. Run with --verbose for detailed output")
            print(f"   4. Check ESP-IDF version compatibility")
            
            return False
            
    except Exception as e:
        print(f"❌ Build failed with exception: {e}")
        import traceback
        if verbose:
            traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description="Build an ESP32 project using ESP-IDF")
    parser.add_argument("--path", help="Path to project directory (default: current directory)")
    parser.add_argument("--target", help="Target chip (esp32, esp32s2, esp32s3, esp32c3, etc.). If not specified, uses default from config.")
    parser.add_argument("--clean", action="store_true", help="Clean build before compiling")
    parser.add_argument("--setup", action="store_true", help="Run setup wizard before building")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    
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
    
    # Build project
    success = build_project(args.path, args.target, args.clean, args.verbose, setup_if_needed)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()