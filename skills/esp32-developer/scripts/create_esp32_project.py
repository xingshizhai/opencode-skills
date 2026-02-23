#!/usr/bin/env python3
"""
Create a new ESP32 project based on ESP-IDF Hello World example.

Usage:
    create_esp32_project.py <project_name> [--target TARGET] [--path PATH] [--setup]

Examples:
    create_esp32_project.py my_project
    create_esp32_project.py my_project --target esp32s3 --path /home/user/projects
    create_esp32_project.py my_project --setup  # Run setup wizard first
"""

import os
import sys
import shutil
import argparse
import subprocess

# Add config manager to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config_manager

def check_esp_idf(setup_if_needed=True):
    """Check if ESP-IDF environment is set up."""
    # Try to get configured IDF_PATH
    idf_path = config_manager.get_configured_idf_path()
    
    if not idf_path and setup_if_needed:
        print("ESP-IDF is not configured.")
        response = input("Would you like to run the setup wizard now? [Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            config = config_manager.interactive_setup()
            if config:
                idf_path = config.get('idf_path')
            else:
                print("Setup cancelled.")
                return None
        else:
            print("Please configure ESP-IDF first.")
            print("Run: python scripts/config_manager.py --setup")
            return None
    
    if not idf_path:
        print("ERROR: ESP-IDF is not configured.")
        print("Please run: python scripts/config_manager.py --setup")
        return None
    
    if not os.path.exists(idf_path):
        print(f"ERROR: IDF_PATH directory does not exist: {idf_path}")
        print("Please reconfigure ESP-IDF: python scripts/config_manager.py --setup")
        return None
    
    return idf_path

def find_hello_world_example(idf_path):
    """Find the hello_world example in ESP-IDF."""
    example_path = os.path.join(idf_path, "examples", "get-started", "hello_world")
    if os.path.exists(example_path):
        return example_path
    
    # Alternative location
    example_path = os.path.join(idf_path, "examples", "get_started", "hello_world")
    if os.path.exists(example_path):
        return example_path
    
    print(f"ERROR: Could not find hello_world example in {idf_path}/examples/")
    return None

def create_project(project_name, target, path, setup_if_needed=True):
    """Create a new ESP32 project."""
    # Load configuration
    config = config_manager.load_config()
    
    # Use default target if not specified
    if not target:
        target = config.get('default_target', 'esp32')
        print(f"Using default target: {target}")
    
    # Determine output directory
    if path:
        output_dir = os.path.join(path, project_name)
    else:
        output_dir = os.path.join(os.getcwd(), project_name)
    
    # Check if directory already exists
    if os.path.exists(output_dir):
        print(f"ERROR: Directory already exists: {output_dir}")
        return False
    
    # Check ESP-IDF environment
    idf_path = check_esp_idf(setup_if_needed)
    if not idf_path:
        return False
    
    # Find hello_world example
    example_path = find_hello_world_example(idf_path)
    if not example_path:
        return False
    
    print(f"Creating ESP32 project '{project_name}'...")
    print(f"  Target: {target}")
    print(f"  Location: {output_dir}")
    
    try:
        # Copy example project
        shutil.copytree(example_path, output_dir)
        print(f"  Copied hello_world example to {output_dir}")
        
        # Update CMakeLists.txt to set target if specified
        if target and target != "esp32":
            cmake_file = os.path.join(output_dir, "CMakeLists.txt")
            if os.path.exists(cmake_file):
                with open(cmake_file, 'r') as f:
                    content = f.read()
                
                # Replace default target
                new_content = content.replace('set(IDF_TARGET "esp32")', f'set(IDF_TARGET "{target}")')
                
                # If set(IDF_TARGET) not found, add it after project()
                if new_content == content:
                    lines = content.split('\n')
                    new_lines = []
                    for line in lines:
                        new_lines.append(line)
                        if line.strip().startswith('project('):
                            new_lines.append(f'set(IDF_TARGET "{target}")')
                    new_content = '\n'.join(new_lines)
                
                with open(cmake_file, 'w') as f:
                    f.write(new_content)
                print(f"  Set target to {target} in CMakeLists.txt")
        
        # Create a simple README
        readme_file = os.path.join(output_dir, "README.md")
        with open(readme_file, 'w') as f:
            f.write(f"# {project_name}\n\n")
            f.write(f"ESP32 project created with ESP-IDF.\n")
            f.write(f"Target: {target}\n\n")
            f.write("## Building\n")
            f.write("```bash\n")
            f.write(f"cd {project_name}\n")
            f.write("idf.py set-target {target}\n")
            f.write("idf.py build\n")
            f.write("```\n")
        
        print(f"\n✅ Project created successfully at {output_dir}")
        print(f"\nNext steps:")
        print(f"  1. cd {output_dir}")
        if target and target != "esp32":
            print(f"  2. idf.py set-target {target}")
        print(f"  3. idf.py menuconfig   # Configure project (optional)")
        print(f"  4. idf.py build")
        print(f"  5. idf.py flash monitor   # Flash and monitor")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to create project: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create a new ESP32 project based on ESP-IDF Hello World example")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--target", help="Target chip (esp32, esp32s2, esp32s3, esp32c3, etc.). If not specified, uses default from config.")
    parser.add_argument("--path", help="Path where project will be created (default: current directory)")
    parser.add_argument("--setup", action="store_true", help="Run setup wizard before creating project")
    
    args = parser.parse_args()
    
    # Run setup wizard if requested
    setup_if_needed = True
    if args.setup:
        config = config_manager.interactive_setup()
        if not config:
            print("Setup cancelled.")
            sys.exit(1)
        setup_if_needed = False  # Already setup
    
    success = create_project(args.project_name, args.target, args.path, setup_if_needed)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()