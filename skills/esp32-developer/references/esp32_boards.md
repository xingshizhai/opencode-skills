# ESP32 Development Boards

## Overview

This document covers common ESP32 development boards and their configurations for ESP-IDF development.

## Board Selection

### ESP32 Family
- **ESP32**: Dual-core, Wi-Fi + Bluetooth Classic + BLE
- **ESP32-S2**: Single-core, USB OTG, Wi-Fi only
- **ESP32-S3**: Dual-core, USB OTG, Wi-Fi + Bluetooth 5.0
- **ESP32-C3**: Single-core RISC-V, Wi-Fi + Bluetooth 5.0
- **ESP32-C6**: Wi-Fi 6 + Bluetooth 5.3 + 802.15.4 (Thread/Zigbee)
- **ESP32-H2**: Bluetooth 5.2 + 802.15.4 (Thread/Zigbee)

## Popular Development Boards

### Espressif Official Boards

#### ESP32-DevKitC
- **Chip**: ESP32
- **Features**: 4MB flash, on-board USB-to-UART, buttons for EN and BOOT
- **Pinout**: All GPIOs exposed
- **Target**: `esp32`
- **Serial Port**: Typically `/dev/ttyUSB0`

#### ESP32-S3-DevKitC-1
- **Chip**: ESP32-S3
- **Features**: 8MB flash, 8MB PSRAM, USB-C, RGB LED
- **Target**: `esp32s3`
- **Serial Port**: Typically `/dev/ttyACM0` (USB-CDC)

#### ESP32-C3-DevKitC-02
- **Chip**: ESP32-C3
- **Features**: 4MB flash, USB-C, RGB LED
- **Target**: `esp32c3`
- **Serial Port**: Typically `/dev/ttyACM0`

### Third-Party Boards

#### NodeMCU-32S
- **Chip**: ESP32
- **Features**: 4MB flash, CP2102 USB-to-UART, breadboard friendly
- **Target**: `esp32`
- **Serial Port**: Typically `/dev/ttyUSB0`

#### TTGO T-Display
- **Chip**: ESP32
- **Features**: 4MB flash, 1.14" ST7789V display, battery connector
- **Target**: `esp32`
- **Notes**: Requires display driver components

#### M5Stack Core
- **Chip**: ESP32
- **Features**: 4MB flash, 2" display, speaker, buttons, grove connectors
- **Target**: `esp32`
- **Notes**: Includes additional peripherals

## Board Configuration

### Setting Target
```bash
# For ESP32
idf.py set-target esp32

# For ESP32-S3
idf.py set-target esp32s3

# For ESP32-C3
idf.py set-target esp32c3
```

### Common Configuration Options

#### Flash Size
```bash
idf.py menuconfig
# Navigate to: Component config → ESP32-specific → Flash size
```

#### PSRAM
```bash
idf.py menuconfig
# Navigate to: Component config → ESP32-specific → Support for external, SPI-connected RAM
```

#### Serial Flasher Config
```bash
idf.py menuconfig
# Navigate to: Serial flasher config
# - Flash SPI mode
# - Flash SPI speed
# - Flash size
```

## Board-Specific Notes

### ESP32-DevKitC
- **Boot Mode**: Hold BOOT button while pressing EN to enter download mode
- **Reset**: Press EN button to reset
- **GPIO0**: Connected to BOOT button (pull down to enter download mode)

### ESP32-S3-DevKitC
- **USB-CDC**: Uses USB serial by default, no external USB-to-UART needed
- **Boot Mode**: Automatically enters download mode when `idf.py flash` is called
- **RGB LED**: Connected to GPIO48

### ESP32-C3-DevKitC
- **USB-CDC**: Uses USB serial
- **Boot Mode**: Automatically enters download mode
- **RGB LED**: Connected to GPIO8

## Serial Port Identification

### Linux
```bash
# List serial ports
ls /dev/ttyUSB* /dev/ttyACM*

# Check with dmesg when connecting board
dmesg | tail -20

# Typical assignments:
# - CP2102/CH340 chips: /dev/ttyUSB0
# - ESP32-S3/C3 USB-CDC: /dev/ttyACM0
```

### macOS
```bash
# List serial ports
ls /dev/cu.*

# Typical assignments:
# - CP2102/CH340: /dev/cu.usbserial-*
# - ESP32-S3/C3 USB-CDC: /dev/cu.usbmodem-*
```

### Windows
- **CP2102/CH340**: COM3, COM4, etc.
- **ESP32-S3/C3 USB-CDC**: COM ports with "USB Serial Device" description

## Flashing Procedures

### Standard Flashing
```bash
idf.py -p /dev/ttyUSB0 flash
```

### Manual Boot Mode
If automatic reset fails:
1. Hold BOOT button
2. Press EN button (while holding BOOT)
3. Release EN button
4. Release BOOT button
5. Run flash command immediately

### Baud Rate
```bash
# Default: 460800
idf.py -p /dev/ttyUSB0 -b 460800 flash

# Slower baud rate for stability
idf.py -p /dev/ttyUSB0 -b 115200 flash
```

## Troubleshooting

### Board Not Recognized
- Check USB cable (some cables are power-only)
- Try different USB port
- Check drivers (CP2102, CH340 drivers may be needed)
- Verify board power LED is on

### Flashing Fails
- Ensure correct serial port
- Try manual boot mode
- Lower baud rate: `-b 115200`
- Check voltage (some boards need 5V, some 3.3V)

### Serial Monitor Not Working
- Check baud rate (usually 115200 for monitor)
- Ensure no other program is using the serial port
- Try resetting the board

## Resources

- [Espressif Hardware Reference](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/)
- [ESP32 Datasheet](https://www.espressif.com/en/products/socs/esp32)
- [ESP32-S3 Datasheet](https://www.espressif.com/en/products/socs/esp32-s3)
- [ESP32-C3 Datasheet](https://www.espressif.com/en/products/socs/esp32-c3)