# 常见串口协议参考

## 协议概述

### 基本概念
- **波特率 (Baud Rate)**: 数据传输速率（位/秒）
- **数据位 (Data Bits)**: 每个字符的位数（通常5-8位）
- **校验位 (Parity)**: 错误检测位（无/奇/偶）
- **停止位 (Stop Bits)**: 字符结束标志（通常1-2位）

### 常用配置
| 设备类型 | 波特率 | 数据位 | 校验位 | 停止位 | 流控制 |
|---------|--------|--------|--------|--------|--------|
| Arduino | 9600/115200 | 8 | 无 | 1 | 无 |
| GPS模块 | 4800/9600 | 8 | 无 | 1 | 无 |
| 工业PLC | 9600/19200 | 8 | 偶/无 | 1 | 有 |
| 蓝牙模块 | 9600/115200 | 8 | 无 | 1 | 无 |
| 智能电表 | 1200/2400 | 8 | 偶 | 1 | 无 |

## NMEA协议（GPS）

### 概述
NMEA 0183标准用于GPS接收器输出定位数据。

### 数据格式
```
$GPRMC,hhmmss.sss,A,llll.llll,N,yyyyy.yyyy,E,速度,航向,ddmmyy,,,A*校验和
```

### 常用语句
- **$GPRMC**: 推荐最小定位信息
- **$GPGGA**: GPS定位数据
- **$GPGSA**: 当前卫星信息
- **$GPGSV**: 卫星状态信息
- **$GPVTG**: 地面速度信息

### 解析示例
```python
def parse_nmea(sentence):
    if not sentence.startswith('$'):
        return None
    
    fields = sentence.strip().split(',')
    sentence_type = fields[0]
    
    if sentence_type == '$GPRMC':
        # 解析GPRMC语句
        time = fields[1]
        status = fields[2]  # A=有效，V=无效
        lat = fields[3]
        lat_dir = fields[4]
        lon = fields[5]
        lon_dir = fields[6]
        speed = fields[7]  # 节
        course = fields[8]  # 度
        date = fields[9]
        
        return {
            'type': 'GPRMC',
            'time': time,
            'status': status,
            'latitude': convert_nmea_to_decimal(lat, lat_dir),
            'longitude': convert_nmea_to_decimal(lon, lon_dir),
            'speed_knots': float(speed) if speed else 0,
            'course': float(course) if course else 0,
            'date': date
        }
    
    return None

def convert_nmea_to_decimal(nmea_coord, direction):
    """将NMEA坐标转换为十进制"""
    if not nmea_coord:
        return 0
    
    # 格式: DDDMM.MMMM
    degrees = int(float(nmea_coord) / 100)
    minutes = float(nmea_coord) - degrees * 100
    decimal = degrees + minutes / 60
    
    if direction in ('S', 'W'):
        decimal = -decimal
    
    return decimal
```

## Modbus RTU协议

### 概述
Modbus RTU用于工业自动化设备通信，使用二进制编码。

### 数据帧格式
```
[设备地址][功能码][数据][CRC校验]
```

### 常用功能码
- **0x01**: 读取线圈状态
- **0x02**: 读取输入状态
- **0x03**: 读取保持寄存器
- **0x04**: 读取输入寄存器
- **0x05**: 写单个线圈
- **0x06**: 写单个寄存器
- **0x0F**: 写多个线圈
- **0x10**: 写多个寄存器

### CRC-16计算
```python
def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

# 验证CRC
def verify_crc(data: bytes) -> bool:
    if len(data) < 2:
        return False
    received_crc = int.from_bytes(data[-2:], 'little')
    calculated_crc = crc16(data[:-2])
    return received_crc == calculated_crc
```

### 请求/响应示例
```python
import struct

def read_holding_registers(slave_id, start_addr, count):
    """读取保持寄存器"""
    # 功能码 0x03
    request = bytes([
        slave_id,          # 设备地址
        0x03,              # 功能码
        (start_addr >> 8) & 0xFF,  # 起始地址高字节
        start_addr & 0xFF,         # 起始地址低字节
        (count >> 8) & 0xFF,       # 寄存器数量高字节
        count & 0xFF               # 寄存器数量低字节
    ])
    
    # 计算CRC
    crc = crc16(request)
    request += crc.to_bytes(2, 'little')
    
    return request

def parse_holding_registers_response(response):
    """解析读取保持寄存器的响应"""
    if len(response) < 5:
        return None
    
    slave_id = response[0]
    function_code = response[1]
    byte_count = response[2]
    
    if function_code != 0x03:
        return None
    
    data = response[3:-2]  # 跳过地址、功能码、字节数和CRC
    registers = []
    
    for i in range(0, byte_count, 2):
        if i + 1 < byte_count:
            value = (data[i] << 8) | data[i + 1]
            registers.append(value)
    
    return {
        'slave_id': slave_id,
        'registers': registers
    }
```

## AT命令协议（蓝牙/GSM模块）

### 概述
AT命令用于控制调制解调器、蓝牙和GSM模块。

### 基本命令
- **AT**: 测试连接（应返回"OK"）
- **AT+NAME?**: 查询设备名称
- **AT+NAME=新名称**: 设置设备名称
- **AT+VERSION?**: 查询版本
- **AT+RESET**: 重置设备
- **AT+BAUD?**: 查询波特率
- **AT+BAUD=波特率**: 设置波特率

### HC-05蓝牙模块示例
```python
def configure_bluetooth(ser):
    # 测试连接
    ser.write(b'AT\r\n')
    time.sleep(0.1)
    response = ser.read_all()
    print(f"AT响应: {response}")
    
    # 查询名称
    ser.write(b'AT+NAME?\r\n')
    time.sleep(0.1)
    response = ser.read_all()
    print(f"名称: {response}")
    
    # 设置波特率为115200
    ser.write(b'AT+BAUD8\r\n')  # 8表示115200
    time.sleep(0.1)
    response = ser.read_all()
    print(f"设置波特率: {response}")
```

## 自定义文本协议

### 简单文本格式
```
COMMAND:参数1,参数2,参数3\n
```

### 解析器示例
```python
def parse_simple_protocol(data):
    lines = data.decode('utf-8', errors='ignore').strip().split('\n')
    commands = []
    
    for line in lines:
        if ':' in line:
            cmd, params_str = line.split(':', 1)
            params = params_str.split(',')
            commands.append({
                'command': cmd.strip(),
                'parameters': [p.strip() for p in params]
            })
    
    return commands
```

### JSON格式
```python
import json

def send_json_command(ser, command, **kwargs):
    data = {'cmd': command, **kwargs}
    json_str = json.dumps(data) + '\n'
    ser.write(json_str.encode('utf-8'))

def read_json_response(ser, timeout=1):
    start_time = time.time()
    buffer = b''
    
    while time.time() - start_time < timeout:
        if ser.in_waiting:
            buffer += ser.read(ser.in_waiting)
            try:
                # 尝试解析完整JSON
                response = json.loads(buffer.decode('utf-8'))
                return response
            except json.JSONDecodeError:
                continue
        time.sleep(0.01)
    
    return None
```

## 二进制协议

### 帧结构
```
[起始符][长度][命令字][数据][校验和][结束符]
```

### 示例实现
```python
class BinaryProtocol:
    START_BYTE = 0xAA
    END_BYTE = 0x55
    
    @staticmethod
    def create_frame(command, data=b''):
        length = 4 + len(data)  # 起始符+长度+命令字+校验和+结束符
        frame = bytearray()
        frame.append(BinaryProtocol.START_BYTE)
        frame.append(length)
        frame.append(command)
        frame.extend(data)
        
        # 计算校验和（简单求和）
        checksum = sum(frame[1:]) & 0xFF  # 跳过起始符
        frame.append(checksum)
        frame.append(BinaryProtocol.END_BYTE)
        
        return bytes(frame)
    
    @staticmethod
    def parse_frame(data):
        if len(data) < 5:
            return None
        
        # 查找起始符
        start_idx = data.find(BinaryProtocol.START_BYTE)
        if start_idx == -1:
            return None
        
        data = data[start_idx:]
        
        if len(data) < 2:
            return None
        
        length = data[1]
        if len(data) < length:
            return None
        
        # 验证结束符
        if data[length - 1] != BinaryProtocol.END_BYTE:
            return None
        
        # 验证校验和
        received_checksum = data[length - 2]
        calculated_checksum = sum(data[1:length - 2]) & 0xFF
        if received_checksum != calculated_checksum:
            return None
        
        command = data[2]
        payload = data[3:length - 2]
        
        return {
            'command': command,
            'payload': payload
        }
```

## 流控制和错误处理

### 硬件流控制 (RTS/CTS)
```python
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    rtscts=True,  # 启用RTS/CTS流控制
    timeout=1
)
```

### 软件流控制 (XON/XOFF)
```python
ser = serial.Serial(
    port='COM3', 
    baudrate=115200,
    xonxoff=True,  # 启用XON/XOFF流控制
    timeout=1
)
```

### 错误处理策略
```python
def robust_serial_communication(port, command, max_retries=3):
    for attempt in range(max_retries):
        try:
            ser = serial.Serial(port, 9600, timeout=1)
            ser.write(command)
            response = ser.read(100)
            ser.close()
            return response
        except serial.SerialException as e:
            print(f"尝试 {attempt + 1} 失败: {e}")
            time.sleep(0.5 * (attempt + 1))  # 指数退避
        except Exception as e:
            print(f"意外错误: {e}")
            break
    
    return None
```

## 协议选择建议

### 根据应用场景选择
- **简单传感器**: 自定义文本协议（易于调试）
- **工业设备**: Modbus RTU（标准、可靠）
- **位置数据**: NMEA（GPS标准）
- **无线模块**: AT命令（广泛支持）
- **高速数据**: 自定义二进制协议（效率高）

### 调试技巧
1. 使用`serial_monitor.py`监控原始数据
2. 验证波特率设置是否正确
3. 检查数据格式（文本/二进制）
4. 使用校验和确保数据完整性
5. 记录通信日志用于分析