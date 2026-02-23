# ESP32 Troubleshooting Guide

## Common Issues and Solutions

### 1. Build Issues

#### "CMake Error: No project specified"
**Cause**: Not in a project directory or missing CMakeLists.txt
**Solution**:
```bash
cd /path/to/your/project
ls CMakeLists.txt  # Verify file exists
idf.py build
```

#### "fatal error: esp_idf_version.h: No such file or directory"
**Cause**: ESP-IDF environment not set up
**Solution**:
```bash
source $IDF_PATH/export.sh
# Verify with:
echo $IDF_PATH
```

#### Python dependency errors
**Cause**: Missing Python packages
**Solution**:
```bash
cd $IDF_PATH
./install.sh
# Or update pip packages:
python -m pip install --upgrade pip
python -m pip install -r $IDF_PATH/requirements.txt
```

#### Build runs out of memory
**Cause**: Insufficient RAM for parallel builds
**Solution**:
```bash
# Reduce parallel jobs
idf.py -j 2 build

# Clean build directory
idf.py fullclean
```

### 2. Flashing Issues

#### "Failed to connect to ESP32: Timed out waiting for packet header"
**Cause**: Wrong serial port, board not in download mode, or connection issue
**Solution**:
1. Verify serial port:
   ```bash
   ls /dev/ttyUSB* /dev/ttyACM*
   idf.py -p /dev/ttyUSB0 flash
   ```
2. Manual download mode:
   - Hold BOOT button
   - Press EN button
   - Release EN button
   - Release BOOT button
   - Run flash command immediately
3. Try lower baud rate:
   ```bash
   idf.py -p /dev/ttyUSB0 -b 115200 flash
   ```
4. Check USB cable (use data cable, not power-only)

#### "Permission denied" on serial port (Linux)
**Cause**: User not in dialout group
**Solution**:
```bash
sudo usermod -a -G dialout $USER
# Log out and log back in

# Temporary fix:
sudo chmod 666 /dev/ttyUSB0
```

#### "A fatal error occurred: Could not open /dev/ttyUSB0"
**Cause**: Port in use by another program
**Solution**:
```bash
# Check if port is in use
sudo lsof /dev/ttyUSB0

# Kill processes using the port
sudo kill -9 <PID>
```

### 3. Serial Monitor Issues

#### No output in serial monitor
**Cause**: Wrong baud rate, board not running, or incorrect port
**Solution**:
1. Check baud rate (usually 115200):
   ```bash
   idf.py -p /dev/ttyUSB0 -b 115200 monitor
   ```
2. Verify board is powered and running
3. Check if code has print statements
4. Try resetting the board (press EN button)

#### Garbled output
**Cause**: Baud rate mismatch
**Solution**:
1. Try common baud rates: 115200, 74880, 9600
2. Check project configuration:
   ```bash
   idf.py menuconfig
   # Navigate to: Component config → ESP32-specific → UART console baud rate
   ```

#### Monitor disconnects frequently
**Cause**: Power issues or USB cable problems
**Solution**:
1. Use shorter, higher quality USB cable
2. Ensure stable power supply
3. Add delay in code to prevent watchdog resets

### 4. Runtime Issues

#### Board resets continuously
**Cause**: Watchdog timeout, stack overflow, or memory corruption
**Solution**:
1. Check serial monitor for error messages
2. Increase task stack size:
   ```c
   xTaskCreate(task_function, "Task", 4096, NULL, 5, NULL);
   ```
3. Disable watchdog for debugging:
   ```c
   // In app_main()
   esp_task_wdt_init(30, false);
   ```

#### Wi-Fi/Bluetooth not working
**Cause**: Configuration issue or antenna connection
**Solution**:
1. Verify Wi-Fi/BT is enabled in menuconfig
2. Check antenna connections (if external antenna)
3. Verify credentials and network settings

#### Memory allocation failures
**Cause**: Insufficient heap memory
**Solution**:
1. Check free heap:
   ```c
   ESP_LOGI(TAG, "Free heap: %d", esp_get_free_heap_size());
   ```
2. Reduce memory usage or enable PSRAM
3. Use memory optimization techniques

### 5. ESP-IDF Environment Issues

#### "Command 'idf.py' not found"
**Cause**: ESP-IDF environment not sourced
**Solution**:
```bash
source $IDF_PATH/export.sh
# Add to ~/.bashrc for permanent setup:
echo "source \$HOME/esp/esp-idf/export.sh" >> ~/.bashrc
```

#### "IDF_PATH not set"
**Cause**: Environment variable not set
**Solution**:
```bash
export IDF_PATH=~/esp/esp-idf
# Verify:
echo $IDF_PATH
```

#### Python version conflicts
**Cause**: Multiple Python versions installed
**Solution**:
```bash
# Use python3 explicitly
python3 -m pip install --upgrade pip

# Check Python version
python --version
python3 --version

# Use virtual environment
python3 -m venv ~/esp/venv
source ~/esp/venv/bin/activate
./install.sh
```

### 6. Hardware Issues

#### Board not powering on
**Cause**: Power supply issue or damaged board
**Solution**:
1. Check USB cable and port
2. Verify power LED is lit
3. Check voltage with multimeter (should be 3.3V)
4. Try different USB port or computer

#### GPIO not working as expected
**Cause**: Pin configuration conflict or hardware issue
**Solution**:
1. Check pin assignments in code vs schematic
2. Verify no conflicts with other peripherals
3. Check pull-up/pull-down resistors
4. Test with simple blink example

#### Unstable behavior
**Cause**: Power fluctuations or noise
**Solution**:
1. Add decoupling capacitors near power pins
2. Use shorter wires for connections
3. Add pull-up/pull-down resistors on floating pins
4. Ensure stable power supply

### 7. Debugging Techniques

#### Enable Core Dump
```bash
idf.py menuconfig
# Navigate to: Component config → ESP32-specific → Core dump destination
# Set to: Flash/UART
```

#### Increase Log Level
```c
// In app_main()
esp_log_level_set("*", ESP_LOG_VERBOSE);
```

#### Use JTAG Debugging
1. Connect JTAG adapter
2. Configure OpenOCD:
   ```bash
   idf.py openocd
   ```
3. Start GDB:
   ```bash
   idf.py gdb
   ```

#### Monitor Task States
```c
// Include header
#include "esp_task_wdt.h"

// Get task list
void print_tasks() {
    char *buffer = malloc(1024);
    vTaskList(buffer);
    printf("Task List:\n%s", buffer);
    free(buffer);
}
```

### 8. Common Error Messages

#### "Guru Meditation Error"
**Cause**: CPU exception (null pointer, illegal instruction, etc.)
**Solution**: Check serial monitor for details and stack trace

#### "assert failed"
**Cause**: Assertion failure in code
**Solution**: Check assert message and location in code

#### "Brownout detector was triggered"
**Cause**: Insufficient voltage
**Solution**: Improve power supply, add capacitors

#### "Task watchdog got triggered"
**Cause**: Task not feeding watchdog
**Solution**: Add vTaskDelay or feed watchdog in long-running tasks

### 9. Resources

- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- [ESP32 Forum](https://esp32.com/)
- [ESP-IDF GitHub Issues](https://github.com/espressif/esp-idf/issues)
- [ESP32 Datasheets](https://www.espressif.com/en/products/socs)

### Quick Reference

```bash
# When in doubt, try this sequence:
1. idf.py fullclean
2. idf.py set-target <chip>
3. idf.py menuconfig  # Check settings
4. idf.py build
5. idf.py -p /dev/ttyUSB0 -b 115200 flash monitor
```