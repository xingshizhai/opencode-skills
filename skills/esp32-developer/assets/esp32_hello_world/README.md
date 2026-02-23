# ESP32 Hello World Project

This is a simple ESP32 Hello World project created with ESP-IDF.

## Project Structure

```
.
├── CMakeLists.txt          # Root CMake file
├── main/
│   ├── CMakeLists.txt     # Component CMake file
│   └── main.c             # Main application source
└── README.md              # This file
```

## Requirements

- ESP-IDF v5.0 or later
- ESP32 development board
- USB cable

## Building the Project

```bash
# Set target (if not default esp32)
idf.py set-target esp32

# Configure (optional)
idf.py menuconfig

# Build
idf.py build
```

## Flashing

Connect your ESP32 board via USB and flash:

```bash
idf.py -p /dev/ttyUSB0 flash
```

## Monitoring

Start serial monitor to see output:

```bash
idf.py -p /dev/ttyUSB0 monitor
```

## Expected Output

The program will:
1. Print "Hello from ESP32!" to serial monitor
2. Blink the onboard LED (if available)
3. Print LED state every second

## Customization

### Change LED Pin

Edit `main/main.c` and change `LED_PIN` definition:

```c
#define LED_PIN 2  // Change to your board's LED pin
```

### Common LED Pins

- ESP32-DevKitC: GPIO2
- ESP32-S3-DevKitC: GPIO48 (RGB LED) or GPIO2
- ESP32-C3-DevKitC: GPIO8 (RGB LED)
- NodeMCU-32S: GPIO2
- TTGO T-Display: GPIO4

### Add More Features

- Add Wi-Fi: See `examples/wifi` in ESP-IDF
- Add Bluetooth: See `examples/bluetooth` in ESP-IDF
- Add sensors: See `examples/peripherals` in ESP-IDF

## Troubleshooting

### No Serial Output
- Check baud rate (default: 115200)
- Verify board is powered
- Check USB cable connection

### Build Errors
- Ensure ESP-IDF environment is set: `source $IDF_PATH/export.sh`
- Clean build: `idf.py fullclean`

### Flashing Issues
- Press BOOT button while flashing if auto-reset fails
- Try lower baud rate: `idf.py -p /dev/ttyUSB0 -b 115200 flash`

## Resources

- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/)
- [ESP32 Hardware Reference](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/)
- [ESP32 Forum](https://esp32.com/)