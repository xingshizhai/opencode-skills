---
name: serial-windows
description: Windows串口设备读写、配置和管理。使用当Claude需要与串口设备交互时：(1) 列出可用串口，(2) 读写串口数据，(3) 配置串口参数（波特率、数据位、停止位等），(4) 监控串口数据流，(5) 与Arduino、传感器、工业设备等串口设备通信。
---

# Serial Windows

## Overview

提供在Windows系统下通过Python pyserial库进行串口设备读写、配置和管理的完整能力。支持COM端口枚举、数据收发、参数配置和实时监控。

## 前置条件

- Python 3.6+
- pyserial库（`pip install pyserial`）
- Windows系统串口设备（物理串口、USB转串口、虚拟串口等）

## 快速开始

### 列出可用串口

```python
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(f"{port.device}: {port.description}")
```

### 简单读取示例

```python
import serial

ser = serial.Serial('COM3', 9600, timeout=1)
try:
    while True:
        data = ser.readline()
        if data:
            print(f"Received: {data.decode('utf-8', errors='ignore').strip()}")
except KeyboardInterrupt:
    ser.close()
```

## 核心任务

### 1. 枚举可用串口

使用`serial.tools.list_ports.comports()`获取所有可用串口。Windows上COM端口名称为`COM1`、`COM2`等。

参考脚本：`scripts/list_ports.py`

### 2. 打开和配置串口

关键参数：
- `port`: 串口名称（如`'COM3'`）
- `baudrate`: 波特率（9600, 115200等）
- `bytesize`: 数据位（`serial.EIGHTBITS`）
- `parity`: 校验位（`serial.PARITY_NONE`）
- `stopbits`: 停止位（`serial.STOPBITS_ONE`）
- `timeout`: 读取超时（秒）
- `write_timeout`: 写入超时（秒）

```python
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,
    write_timeout=1
)
```

### 3. 读取串口数据

多种读取方式：
- `read(size)`: 读取指定字节数
- `readline()`: 读取一行（直到换行符）
- `readlines()`: 读取多行
- `read_all()`: 读取所有可用数据

### 4. 写入串口数据

```python
ser.write(b'Hello World\r\n')
ser.write("命令字符串".encode('utf-8'))
```

### 5. 实时监控串口数据

参考脚本：`scripts/serial_monitor.py`

### 6. 与常见设备交互

- **Arduino**: 115200波特率，文本协议
- **GPS模块**: 9600波特率，NMEA协议
- **工业传感器**: Modbus RTU，特定协议

## 故障排除

### 常见问题

1. **权限拒绝**: 以管理员身份运行或调整COM端口权限
2. **端口不存在**: 确认设备管理器中的COM端口号
3. **数据乱码**: 检查波特率、数据位、校验位设置
4. **读取超时**: 调整`timeout`参数或检查设备输出

### Windows特定问题

- 虚拟串口（如com0com）需要额外驱动
- 蓝牙串口可能显示为`COM4`、`COM5`等
- USB转串口设备需要安装对应驱动程序

## 脚本参考

本技能包含以下实用脚本：

- `scripts/list_ports.py`: 列出所有可用串口及详细信息
- `scripts/serial_monitor.py`: 实时监控串口数据流
- `scripts/send_command.py`: 向串口发送命令并接收响应

使用前确保pyserial已安装：`pip install pyserial`

## 资源结构

### scripts/
包含可直接执行的Python脚本：
- `list_ports.py`: 列出所有可用串口及详细信息
- `serial_monitor.py`: 实时监控串口数据流
- `send_command.py`: 向串口发送命令并接收响应

### references/
参考文档：
- `windows_specific.md`: Windows系统串口配置和故障排除指南
- `common_protocols.md`: 常见串口协议（NMEA、Modbus RTU等）

### assets/
资源文件（本技能暂不需要，目录可保留为空）
