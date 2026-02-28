# Windows串口配置和故障排除指南

## Windows串口系统概述

### COM端口命名
Windows使用`COMx`格式命名串口（x为数字）：
- `COM1` ~ `COM9`: 传统串口
- `COM10`及以上: 扩展串口（包括USB转串口、虚拟串口等）
- 蓝牙串口通常显示为`COM4`、`COM5`等

### 设备管理器查看
1. 右键点击"开始"菜单 → "设备管理器"
2. 展开"端口 (COM和LPT)"查看所有串口
3. 右键点击端口 → "属性"查看详细信息

## 串口权限问题

### 管理员权限
某些串口需要管理员权限才能访问：
- 以管理员身份运行Python脚本或命令提示符
- 或调整串口安全设置

### 调整串口权限
```powershell
# 查看当前权限
$acl = Get-Acl -Path "\\.\COM3"
$acl.Access

# 添加用户权限（需要管理员权限）
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule("Users","FullControl","Allow")
$acl.SetAccessRule($rule)
Set-Acl -Path "\\.\COM3" -AclObject $acl
```

## 虚拟串口配置

### com0com（虚拟串口对）
1. 下载安装com0com：https://sourceforge.net/projects/com0com/
2. 安装后创建虚拟串口对（如COM10 ↔ COM11）
3. 可用于测试串口通信

### 其他虚拟串口工具
- **Virtual Serial Port Driver (VSPD)**: 商业软件，功能强大
- **socat (Windows版)**: 开源工具，支持多种转发

## USB转串口驱动

### 常见芯片及驱动
| 芯片型号 | 厂商 | 驱动下载 |
|---------|------|---------|
| FTDI FT232 | FTDI | https://www.ftdichip.com/Drivers/D2XX.htm |
| CP210x | Silicon Labs | https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers |
| CH340/CH341 | WCH | http://www.wch-ic.com/downloads/CH341SER_EXE.html |
| PL2303 | Prolific | https://www.prolific.com.tw/US/ShowProduct.aspx?p_id=225&pcid=41 |

### 驱动安装问题
1. **驱动签名错误**: Windows可能阻止未签名驱动
   - 高级启动 → 禁用驱动签名强制
   - 或使用经过微软认证的驱动版本
2. **设备管理器黄色感叹号**: 驱动不匹配或损坏
   - 卸载设备 → 重新插拔 → 自动安装
   - 或手动指定驱动位置

## PowerShell串口管理

### 列出串口
```powershell
Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID, Description
```

### 查看串口详细信息
```powershell
Get-WmiObject Win32_PnPEntity | Where-Object {$_.Name -like "*COM*"} | Select-Object Name, Status, ConfigManagerErrorCode
```

### 重启串口设备
```powershell
# 禁用串口
Disable-PnpDevice -InstanceId "(串口设备实例ID)" -Confirm:$false

# 启用串口  
Enable-PnpDevice -InstanceId "(串口设备实例ID)" -Confirm:$false
```

## 注册表配置

### 串口超时设置
```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Serial
```

### 修改COM端口号
1. 设备管理器 → 端口属性 → 端口设置 → 高级
2. 修改COM端口号（需要重启生效）
3. 或通过注册表修改：
   ```
   HKEY_LOCAL_MACHINE\HARDWARE\DEVICEMAP\SERIALCOMM
   ```

## 常见错误及解决方案

### "Access is denied"（访问被拒绝）
1. 以管理员身份运行程序
2. 检查串口是否被其他程序占用
3. 调整串口安全权限

### "The port does not exist"（端口不存在）
1. 检查设备管理器中端口是否存在
2. 重新插拔USB转串口设备
3. 检查驱动是否正常安装

### "The parameter is incorrect"（参数错误）
1. 检查波特率、数据位等参数是否支持
2. 某些串口不支持高波特率（如115200以上）
3. 尝试标准配置：9600-8-N-1

### "Device does not exist"（设备不存在）
1. 串口可能被禁用
2. 在设备管理器中启用设备
3. 或硬件故障

## 性能优化

### 缓冲区设置
```python
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    # 调整缓冲区大小
    inter_byte_timeout=0.1,
    # Windows特定设置
    exclusive=True
)
```

### 提高读取性能
1. 使用`read()`代替`readline()`避免搜索换行符
2. 适当调整`timeout`值
3. 使用多线程处理数据接收

## 测试工具推荐

### Windows内置工具
1. **超级终端 (HyperTerminal)**: 旧版Windows自带
2. **PuTTY**: 免费开源，支持串口
3. **Tera Term**: 功能丰富的终端软件

### Python测试脚本
使用本技能提供的脚本：
```bash
# 列出串口
python scripts/list_ports.py

# 监控串口数据
python scripts/serial_monitor.py COM3 -b 115200

# 发送测试命令
python scripts/send_command.py COM3 -c "AT\r\n"
```

## 硬件连接检查

### 引脚定义（DB9接口）
```
引脚1: CD  (Carrier Detect)
引脚2: RXD (Receive Data) ← 接收
引脚3: TXD (Transmit Data) → 发送
引脚4: DTR (Data Terminal Ready)
引脚5: GND (Ground) ← 地线
引脚6: DSR (Data Set Ready)
引脚7: RTS (Request To Send)
引脚8: CTS (Clear To Send)
引脚9: RI  (Ring Indicator)
```

### 连接方式
- **直连电缆**: 2↔3, 3↔2, 5↔5（用于两台计算机通信）
- **null modem**: 交叉连接引脚
- **USB转串口**: 通常只需连接RXD、TXD、GND

## 日志和调试

### 启用串口日志
```powershell
# 启用串口调试日志
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Serial" /v "DebugFlags" /t REG_DWORD /d 1 /f

# 查看系统日志
Get-EventLog -LogName System -Source "Serial" -Newest 10
```

### Python调试
```python
import logging
logging.basicConfig(level=logging.DEBUG)
import serial
# 现在serial库会输出调试信息
```