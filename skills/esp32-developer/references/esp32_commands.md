# ESP-IDF Command Reference

## Overview

This document lists the most commonly used `idf.py` commands for ESP32 development with ESP-IDF.

## Basic Project Commands

### `idf.py create-project`
Create a new project from a template (requires ESP-IDF v5.0+).
```bash
idf.py create-project my_project --path /path/to/projects
```

### `idf.py set-target`
Set the target chip for the project.
```bash
idf.py set-target esp32
idf.py set-target esp32s3
idf.py set-target esp32c3
```

### `idf.py build`
Build the project.
```bash
idf.py build
```

### `idf.py clean`
Clean the build output.
```bash
idf.py clean        # Clean build directory
idf.py fullclean    # Clean build directory and sdkconfig
```

### `idf.py flash`
Flash the firmware to the device.
```bash
idf.py flash                    # Auto-detect port
idf.py -p /dev/ttyUSB0 flash   # Specify port
idf.py -b 460800 flash         # Specify baud rate
```

### `idf.py monitor`
Start serial monitor.
```bash
idf.py monitor
idf.py -p /dev/ttyUSB0 monitor
idf.py -b 115200 monitor
```

### `idf.py flash monitor`
Flash and start monitor in one command.
```bash
idf.py flash monitor
```

## Configuration Commands

### `idf.py menuconfig`
Interactive project configuration.
```bash
idf.py menuconfig
```

### `idf.py defconfig`
Set default configuration.
```bash
idf.py defconfig
```

### `idf.py save-defconfig`
Save current configuration as default.
```bash
idf.py save-defconfig
```

## Component Management

### `idf.py create-component`
Create a new component.
```bash
idf.py create-component my_component
```

### `idf.py list-components`
List all components in the project.
```bash
idf.py list-components
```

## Debugging Commands

### `idf.py gdb`
Start GDB debugger.
```bash
idf.py gdb
```

### `idf.py openocd`
Start OpenOCD for debugging.
```bash
idf.py openocd
```

### `idf.py size`
Display size analysis of the firmware.
```bash
idf.py size
idf.py size-components
idf.py size-files
```

### `idf.py app`
Application-related commands.
```bash
idf.py app bootloader          # Build bootloader only
idf.py app partition-table     # Build partition table only
```

## Utility Commands

### `idf.py --version`
Show ESP-IDF version.
```bash
idf.py --version
```

### `idf.py --help`
Show help information.
```bash
idf.py --help
idf.py <command> --help
```

### `idf.py python-clean`
Clean Python temporary files.
```bash
idf.py python-clean
```

## Common Command Combinations

### Complete development workflow:
```bash
# 1. Create project
cp -r $IDF_PATH/examples/get-started/hello_world my_project
cd my_project

# 2. Set target (if not default esp32)
idf.py set-target esp32s3

# 3. Configure (optional)
idf.py menuconfig

# 4. Build
idf.py build

# 5. Flash and monitor
idf.py -p /dev/ttyUSB0 flash monitor
```

### Debug workflow:
```bash
# Build with debug symbols
idf.py -DCMAKE_BUILD_TYPE=Debug build

# Start OpenOCD
idf.py openocd

# In another terminal: start GDB
idf.py gdb
```

### Production build:
```bash
# Build with size optimization
idf.py -DCMAKE_BUILD_TYPE=Release build

# Get size report
idf.py size

# Generate binary for OTA
idf.py app bootloader partition-table
```

## Environment Variables

### `IDF_PATH`
Path to ESP-IDF installation.
```bash
export IDF_PATH=~/esp/esp-idf
```

### `IDF_TARGET`
Default target chip.
```bash
export IDF_TARGET=esp32s3
```

### `ESP_PORT`
Default serial port.
```bash
export ESP_PORT=/dev/ttyUSB0
```

## Tips and Tricks

### Speeding up builds:
```bash
# Enable ccache
export CCACHE_ENABLE=1

# Parallel builds
idf.py -j $(nproc) build
```

### Dealing with serial port permissions (Linux):
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Or use udev rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="303a", MODE="0666"' | sudo tee /etc/udev/rules.d/99-esp32.rules
sudo udevadm control --reload-rules
```

### Saving configuration for different targets:
```bash
# Build for esp32
idf.py set-target esp32
idf.py menuconfig
cp sdkconfig sdkconfig.esp32

# Build for esp32s3
idf.py set-target esp32s3
idf.py menuconfig
cp sdkconfig sdkconfig.esp32s3

# Switch between configurations
cp sdkconfig.esp32 sdkconfig
idf.py build
```