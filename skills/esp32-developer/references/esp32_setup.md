# ESP-IDF Setup Guide

## Overview

ESP-IDF (Espressif IoT Development Framework) is the official development framework for ESP32, ESP32-S, ESP32-C, and ESP32-H series SoCs. This guide covers installation and setup for Linux, macOS, and Windows.

## Prerequisites

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

### macOS
```bash
brew install cmake ninja dfu-util ccache
```

### Windows
- Install Python 3.11+ from [python.org](https://python.org)
- Install Git from [git-scm.com](https://git-scm.com/)
- Install ESP-IDF Tools Installer from [Espressif](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/windows-setup.html)

## Installation Methods

### Method 1: Using ESP-IDF Installer (Recommended)
```bash
mkdir -p ~/esp
cd ~/esp
wget https://dl.espressif.com/dl/esp-idf/install.sh
chmod +x install.sh
./install.sh
```

### Method 2: Manual Installation
```bash
mkdir -p ~/esp
cd ~/esp
git clone --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh esp32,esp32s2,esp32s3,esp32c3
```

### Method 3: Using VSCode Extension
1. Install Visual Studio Code
2. Install "Espressif IDF" extension
3. Follow extension setup wizard

## Environment Setup

After installation, you need to set up the environment:

### Permanent Setup (Add to ~/.bashrc or ~/.zshrc)
```bash
echo "source $HOME/esp/esp-idf/export.sh > /dev/null 2>&1" >> ~/.bashrc
```

### Temporary Setup (Each terminal session)
```bash
source $HOME/esp/esp-idf/export.sh
```

## Verification

Check if ESP-IDF is properly installed:
```bash
idf.py --version
printenv IDF_PATH
```

## Project Structure

A typical ESP-IDF project structure:
```
my_project/
├── CMakeLists.txt          # Main CMake file
├── sdkconfig              # Project configuration
├── main/
│   ├── CMakeLists.txt     # Component CMake file
│   ├── main.c             # Main application source
│   └── component.mk       # Component configuration (legacy)
├── build/                 # Build output directory
└── other components...
```

## Creating Your First Project

```bash
# Create project from example
cp -r $IDF_PATH/examples/get-started/hello_world my_project
cd my_project

# Configure (optional)
idf.py menuconfig

# Build
idf.py build

# Flash
idf.py -p /dev/ttyUSB0 flash

# Monitor
idf.py -p /dev/ttyUSB0 monitor
```

## Common Issues

### Permission Denied on Serial Port (Linux)
```bash
sudo usermod -a -G dialout $USER
# Log out and log back in
```

### Python Version Issues
Ensure Python 3.8+ is installed and set as default.

### Build Failures
- Clean build: `idf.py fullclean`
- Check dependencies: `./install.sh` to reinstall tools

## Next Steps

- Explore examples in `$IDF_PATH/examples/`
- Read ESP-IDF Programming Guide
- Check ESP32 forums for community support