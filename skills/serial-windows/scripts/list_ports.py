#!/usr/bin/env python3
"""
列出Windows系统所有可用串口及详细信息
"""

import serial.tools.list_ports

def list_serial_ports(verbose=True):
    """列出所有可用串口
    
    Args:
        verbose: 是否显示详细信息
    """
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("未找到可用串口")
        return []
    
    print(f"找到 {len(ports)} 个串口:")
    print("-" * 80)
    
    for i, port in enumerate(ports, 1):
        print(f"{i}. 设备: {port.device}")
        print(f"   描述: {port.description}")
        print(f"   硬件ID: {port.hwid}")
        if port.manufacturer:
            print(f"   制造商: {port.manufacturer}")
        if port.product:
            print(f"   产品: {port.product}")
        if port.serial_number:
            print(f"   序列号: {port.serial_number}")
        if port.location:
            print(f"   位置: {port.location}")
        if port.interface:
            print(f"   接口: {port.interface}")
        print()
    
    return ports

def get_port_by_name(port_name):
    """通过端口名称获取端口信息
    
    Args:
        port_name: 端口名称，如 'COM3'
    
    Returns:
        端口对象或None
    """
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if port.device == port_name:
            return port
    return None

if __name__ == "__main__":
    try:
        ports = list_serial_ports()
        
        # 提供交互式选择示例
        if ports:
            print("\n使用示例:")
            print("  python -c \"import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])\"")
            print("\n在代码中获取端口列表:")
            print("  ports = list(serial.tools.list_ports.comports())")
            print("  for port in ports:")
            print("      print(f'{port.device}: {port.description}')")
            
    except ImportError:
        print("错误: 未找到pyserial库")
        print("请安装: pip install pyserial")
        exit(1)
    except Exception as e:
        print(f"错误: {e}")
        exit(1)