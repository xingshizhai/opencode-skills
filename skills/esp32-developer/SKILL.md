---
name: esp32-developer
description: "ESP32 development and debugging with ESP-IDF framework. Use when working with ESP32 microcontrollers for: (1) Creating new ESP32 projects with interactive ESP-IDF version selection, (2) Building and compiling firmware with configurable target chips, (3) Flashing to development boards with auto-detected serial ports, (4) Serial monitoring and log analysis with filtering, (5) Troubleshooting ESP32 issues. Supports ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6, ESP32-H2 chips and popular development boards with interactive configuration wizard."
---

# ESP32 Development with ESP-IDF

## Overview

This skill provides comprehensive support for ESP32 development using the official ESP-IDF framework. It covers project creation, building, flashing, debugging, and troubleshooting for ESP32 family chips (ESP32, ESP32-S2/S3, ESP32-C3/C6, ESP32-H2). Includes interactive configuration wizard for ESP-IDF version selection and chip type configuration.

**Enhanced Features:**
- **Automatic environment setup**: No need to manually source `export.sh`
- **Non-interactive monitoring**: PySerial-based monitoring works in environments like opencode
- **Better error handling**: Detailed troubleshooting tips for common issues
- **Improved UX**: Emoji feedback, clear instructions, progress indicators
- **Platform support**: Linux, macOS, Windows serial port detection
- **Flexible monitoring**: Choose between `idf.py monitor` or `pyserial` methods
- **Project validation**: Ensure projects are valid before building/flashing

**Key Improvements from v1:**
1. **esp32_utils.py**: Shared utilities for all scripts
2. **Auto environment setup**: Scripts handle ESP-IDF sourcing automatically
3. **PySerial support**: Monitor works in non-interactive terminals
4. **Better diagnostics**: Detailed error messages and troubleshooting
5. **Platform compatibility**: Cross-platform serial port detection

## Configuration

### First-Time Setup
Before using the skill, run the configuration wizard to set up your ESP-IDF environment:

```bash
python scripts/config_manager.py --setup
```

The wizard will:
1. Detect ESP-IDF installations and versions
2. Let you select which ESP-IDF installation to use
3. Set default ESP32 chip target (esp32, esp32s3, esp32c3, etc.)
4. Configure default serial port (optional)

### Configuration File
Settings are saved to `~/.esp32-developer-config.json`. You can:
- View config: `python scripts/config_manager.py --show`
- Reset config: `python scripts/config_manager.py --reset`
- Get IDF_PATH: `python scripts/config_manager.py --path`

### Using Configuration in Scripts
All scripts (`create_esp32_project.py`, `build_esp32_project.py`, etc.) will:
- Use configured IDF_PATH automatically
- **Automatically setup ESP-IDF environment** without manual sourcing
- Use default target chip if not specified
- Use default serial port if not specified (with auto-detection fallback)
- Prompt for setup if not configured (with `--setup` option to force wizard)
- Provide better error messages and troubleshooting tips

## Quick Start

### Prerequisites
1. Install ESP-IDF (see [ESP-IDF Setup Guide](references/esp32_setup.md))
2. **Optional**: Set up environment manually: `source $IDF_PATH/export.sh` (skill scripts handle this automatically)
3. Connect ESP32 board via USB
4. Install pyserial for non-interactive monitoring: `pip install pyserial` (optional, but recommended)

### Common Workflows

**Create and run a Hello World project (recommended):**
```bash
# Configure ESP-IDF first (if not already configured)
python scripts/config_manager.py --setup

# Create a new project
python scripts/create_esp32_project.py my_project --target esp32

cd my_project

# Build the project
python scripts/build_esp32_project.py

# Flash to board (auto-detects port)
python scripts/flash_esp32.py

# Monitor output (non-interactive)
python scripts/monitor_serial.py --method pyserial
```

**Quick workflow with skill scripts:**
```bash
# One-liner: build, flash, and monitor
python scripts/build_esp32_project.py && \
python scripts/flash_esp32.py --monitor

# For non-interactive environments:
python scripts/flash_esp32.py && \
python scripts/monitor_serial.py --method pyserial --timeout 10
```

**Or use ESP-IDF commands directly:**
```bash
# Copy example
cp -r $IDF_PATH/examples/get-started/hello_world my_project
cd my_project

# Build and flash
idf.py set-target esp32
idf.py build
idf.py flash monitor
```

## Creating ESP32 Projects

### Using the Project Creation Script
The `scripts/create_esp32_project.py` script creates a new ESP32 project from the official Hello World example with interactive configuration support:

```bash
python scripts/create_esp32_project.py <project_name> [--target TARGET] [--path PATH] [--setup]
```

**Features:**
- Uses configured IDF_PATH from `~/.esp32-developer-config.json`
- If no target specified, uses default target from config
- Prompts for ESP-IDF setup if not configured (or use `--setup` to force wizard)
- Detects ESP-IDF version automatically

**Examples:**
```bash
# Create project with interactive setup (if not configured)
python scripts/create_esp32_project.py my_app

# Run setup wizard first, then create project
python scripts/create_esp32_project.py my_app --setup

# Create ESP32-S3 project in specific directory
python scripts/create_esp32_project.py my_s3_app --target esp32s3 --path ~/projects

# Create project using default target from config
python scripts/create_esp32_project.py my_app  # Uses configured default target
```

### Manual Project Creation
1. Copy from ESP-IDF examples: `cp -r $IDF_PATH/examples/get-started/hello_world my_project`
2. Update CMakeLists.txt for your target chip
3. Modify main.c for your application

### Project Template
A template project is available in `assets/esp32_hello_world/` containing:
- Basic CMakeLists.txt files
- Hello World main.c with LED blinking
- README with instructions

## Building and Compiling

### Using the Build Script
The `scripts/build_esp32_project.py` script handles building with proper environment checks and configuration support:

```bash
python scripts/build_esp32_project.py [--path PROJECT_PATH] [--target TARGET] [--clean] [--setup] [--verbose]
```

**Enhanced Features:**
- Automatic ESP-IDF environment setup without manual sourcing
- Better error handling with detailed troubleshooting tips
- Project validation to ensure it's a valid ESP-IDF project
- Progress feedback and build summary with binary sizes
- Verbose mode for detailed output

**Examples:**
```bash
# Build current directory project (uses default target from config)
python scripts/build_esp32_project.py

# Run setup wizard first, then build
python scripts/build_esp32_project.py --setup

# Build specific project with target
python scripts/build_esp32_project.py --path ~/projects/my_app --target esp32s3

# Clean build with verbose output
python scripts/build_esp32_project.py --clean --verbose

# Build with detailed error reporting
python scripts/build_esp32_project.py --verbose
```

### Manual Building
```bash
# Set target (if not default esp32)
idf.py set-target <chip>

# Configure (optional)
idf.py menuconfig

# Build
idf.py build

# Parallel build for speed
idf.py -j $(nproc) build
```

### Build Output
- Binaries: `build/bin/` (`.bin`, `.elf` files)
- Map file: `build/<project_name>.map`
- Size report: `idf.py size`

## Flashing to Development Board

### Using the Flash Script
The `scripts/flash_esp32.py` script handles flashing with automatic port detection and configuration support:

```bash
python scripts/flash_esp32.py [--port SERIAL_PORT] [--baud BAUD_RATE] [--path PROJECT_PATH] 
                   [--monitor] [--setup] [--verbose] [--no-reset]
```

**Enhanced Features:**
- Platform-specific serial port detection (Linux, macOS, Windows)
- Better error handling with detailed troubleshooting tips
- Project validation to ensure it's built before flashing
- Flash verification tips and post-flash instructions
- No-reset option for boards with problematic auto-reset

**Examples:**
```bash
# Flash with auto-detected port
python scripts/flash_esp32.py

# Run setup wizard first, then flash
python scripts/flash_esp32.py --setup

# Specify port and baud rate
python scripts/flash_esp32.py --port /dev/ttyUSB0 --baud 460800

# Flash with verbose output
python scripts/flash_esp32.py --port /dev/ttyUSB0 --verbose

# Flash without auto-reset (press BOOT button manually)
python scripts/flash_esp32.py --port /dev/ttyUSB0 --no-reset

# Windows example
python scripts/flash_esp32.py --port COM3 --baud 115200
```

### Manual Flashing
```bash
# Auto-detect port
idf.py flash

# Specify port
idf.py -p /dev/ttyUSB0 flash

# Specify baud rate
idf.py -p /dev/ttyUSB0 -b 460800 flash

# Flash and monitor
idf.py flash monitor
```

### Board-Specific Notes
- **ESP32-DevKitC**: May require BOOT button press for flashing
- **ESP32-S3/C3-DevKitC**: USB-CDC, auto-reset usually works
- **Third-party boards**: Check schematics for correct GPIO0/EN connections

See [ESP32 Boards Reference](references/esp32_boards.md) for details.

## Serial Monitoring and Debugging

### Using the Monitor Script
The `scripts/monitor_serial.py` script provides enhanced serial monitoring with filtering, logging, and configuration support:

```bash
python scripts/monitor_serial.py [--port SERIAL_PORT] [--baud BAUD_RATE] [--path PROJECT_PATH] 
                      [--filter PATTERN] [--save LOG_FILE] [--no-color] [--setup]
                      [--method {idf,pyserial}] [--timeout SECONDS] [--exit-on ERROR_PATTERN]
```

**Enhanced Features:**
- **Dual monitoring methods**: `idf.py monitor` (interactive) or `pyserial` (non-interactive)
- Platform-specific serial port detection
- Real-time filtering with regex patterns
- Log saving to file with timestamp
- Timeout and exit-on-pattern options
- Works in non-interactive environments (like opencode)

**Examples:**
```bash
# Basic monitor with auto-detected port (uses pyserial by default)
python scripts/monitor_serial.py

# Run setup wizard first, then monitor
python scripts/monitor_serial.py --setup

# Monitor with error filtering
python scripts/monitor_serial.py --filter "error|warn|fail"

# Save log to file with timeout
python scripts/monitor_serial.py --save debug.log --timeout 30

# Monitor specific port with pyserial method
python scripts/monitor_serial.py --port /dev/ttyUSB0 --baud 115200 --method pyserial

# Monitor and exit on panic
python scripts/monitor_serial.py --exit-on "panic|abort"

# Use idf.py monitor (interactive terminals only)
python scripts/monitor_serial.py --method idf --no-color
```

### Manual Monitoring
```bash
# Start monitor
idf.py monitor

# Specify port and baud rate
idf.py -p /dev/ttyUSB0 -b 115200 monitor

# Exit monitor: Ctrl+]
```

### Log Analysis
- Default baud rate: 115200 (application), 74880 (boot messages)
- **For non-interactive environments**: Use `--method pyserial` option
- Use `ESP_LOGI()`, `ESP_LOGW()`, `ESP_LOGE()` for structured logging
- Enable verbose logging: `esp_log_level_set("*", ESP_LOG_VERBOSE)`
- **Filtering**: Use `--filter` option to show only specific messages (errors, warnings, etc.)
- **Log saving**: Use `--save` option to capture logs to file for later analysis

## Troubleshooting and Common Issues

### Quick Diagnostics
1. Check ESP-IDF environment: `idf.py --version`
2. Verify serial port: `ls /dev/ttyUSB* /dev/ttyACM*`
3. Check board power LED
4. Monitor boot messages

### Common Problems
- **Flashing timeout**: Press BOOT button during flash, use lower baud rate, try `--no-reset` option
- **Permission denied**: Add user to dialout group: `sudo usermod -a -G dialout $USER`
- **Build errors**: Clean build: `idf.py fullclean`, check CMakeLists.txt
- **No serial output**: Check baud rate (115200 for app, 74880 for boot), verify code has print statements
- **idf.py monitor fails in non-interactive environment**: Use `--method pyserial` option
- **Serial port not detected**: Check cable, try different port, ensure drivers installed

### Debug Techniques
1. Enable core dumps in menuconfig
2. Use JTAG debugging with OpenOCD
3. Add diagnostic prints: `printf("Debug: value=%d\n", variable);`
4. Check free heap: `esp_get_free_heap_size()`

See [Troubleshooting Guide](references/esp32_troubleshooting.md) for detailed solutions.

## Reference Materials

### Included References
Load these references as needed for specific tasks:

1. **[ESP-IDF Setup Guide](references/esp32_setup.md)** - Installation and environment setup
2. **[ESP-IDF Command Reference](references/esp32_commands.md)** - Complete `idf.py` command list
3. **[ESP32 Boards Reference](references/esp32_boards.md)** - Development board specifications
4. **[Troubleshooting Guide](references/esp32_troubleshooting.md)** - Common issues and solutions

### ESP-IDF Resources
- [Official Documentation](https://docs.espressif.com/projects/esp-idf/)
- [API Reference](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/)
- [Examples Directory](https://github.com/espressif/esp-idf/tree/master/examples)
- [ESP32 Forum](https://esp32.com/)

## Scripts Overview

### `scripts/config_manager.py`
Configuration manager for ESP-IDF setup. Handles ESP-IDF installation detection, version selection, and user preferences. Run `python scripts/config_manager.py --setup` for interactive configuration wizard.

### `scripts/esp32_utils.py`
**New**: Shared utility module providing common functions for ESP32 development:
- Automatic ESP-IDF environment setup
- Platform-specific serial port detection
- Project validation and information
- Unified idf.py command execution
- Formatting helpers and utilities

### `scripts/create_esp32_project.py`
Creates new ESP32 projects from Hello World example with target chip configuration and interactive setup support.

### `scripts/build_esp32_project.py` (Enhanced)
Builds ESP32 projects with enhanced features:
- Automatic environment setup
- Better error handling with troubleshooting tips
- Project validation
- Progress feedback and build summary

### `scripts/flash_esp32.py` (Enhanced)
Flashes firmware to ESP32 boards with enhanced features:
- Platform-specific port detection
- Better error handling
- Flash verification tips
- No-reset option support

### `scripts/monitor_serial.py` (Enhanced)
Monitors serial output with enhanced features:
- Dual monitoring methods (idf.py or pyserial)
- Works in non-interactive environments
- Filtering, logging, timeout options
- Exit-on-pattern capability

## Using Bundled Resources

### Templates
- `assets/esp32_hello_world/` - Minimal Hello World project template
- Copy and customize for new projects

### References
- Load reference files when specific information is needed
- Use grep patterns to find relevant sections

### Direct ESP-IDF Usage
When scripts aren't needed, use standard ESP-IDF commands:
```bash
# Complete workflow
cp -r $IDF_PATH/examples/get-started/hello_world my_project
cd my_project
idf.py set-target esp32
idf.py menuconfig
idf.py build
idf.py flash monitor
```

**When to use skill scripts vs direct commands:**
- **Use skill scripts**: For consistent environment setup, better error handling, non-interactive environments
- **Use direct commands**: When you need full control, interactive development, or advanced features
- **Special cases**: Use `--method pyserial` when `idf.py monitor` fails in non-interactive terminals

## Best Practices

### Project Organization
1. Keep main application in `main/` directory
2. Create separate components for reusable functionality
3. Use version control (git)
4. Document configuration changes in README

### Development Workflow
1. Test with Hello World first
2. Incrementally add features
3. Use serial monitor for debugging (use `--method pyserial` in non-interactive environments)
4. Regular commits with descriptive messages
5. **Use skill scripts** for consistent environment setup and error handling
6. Enable `--verbose` flag for detailed debugging information

### Performance Optimization
1. Enable PSRAM if available
2. Use `-j` option for parallel builds
3. Enable ccache: `export CCACHE_ENABLE=1`
4. Remove unused components to reduce binary size

### Maintenance
1. Update ESP-IDF regularly
2. Check for deprecated APIs
3. Test with multiple board variants
4. Keep documentation updated
