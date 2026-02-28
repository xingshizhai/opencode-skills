#!/usr/bin/env python3
"""
实时监控串口数据流
支持显示原始数据和文本数据
"""

import serial
import argparse
import sys
from datetime import datetime

def monitor_serial(port, baudrate=9600, timeout=1, show_hex=False, 
                   show_timestamp=True, show_line_numbers=True):
    """监控串口数据
    
    Args:
        port: 串口名称，如 'COM3'
        baudrate: 波特率，默认9600
        timeout: 读取超时，默认1秒
        show_hex: 是否显示十六进制数据
        show_timestamp: 是否显示时间戳
        show_line_numbers: 是否显示行号
    """
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout
        )
    except serial.SerialException as e:
        print(f"无法打开串口 {port}: {e}")
        print("请检查:")
        print("  1. 串口名称是否正确")
        print("  2. 串口是否被其他程序占用")
        print("  3. 是否有访问权限")
        return
    
    print(f"开始监控串口 {port} ({baudrate} baud)")
    print("按 Ctrl+C 停止监控")
    print("-" * 60)
    
    line_count = 0
    
    try:
        while True:
            # 读取数据
            data = ser.read(ser.in_waiting or 1)
            
            if data:
                line_count += 1
                
                # 构建前缀
                prefix = ""
                if show_timestamp:
                    prefix += f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] "
                if show_line_numbers:
                    prefix += f"#{line_count:04d} "
                
                # 显示文本数据
                try:
                    text = data.decode('utf-8', errors='replace').replace('\r', '\\r').replace('\n', '\\n')
                    if text.strip():
                        print(f"{prefix}TEXT: {text}")
                except:
                    pass
                
                # 显示十六进制数据
                if show_hex:
                    hex_str = ' '.join(f'{b:02X}' for b in data)
                    print(f"{prefix}HEX:  {hex_str}")
                
                # 显示原始字节长度
                print(f"{prefix}RAW:  {len(data)} bytes")
                print()
                
    except KeyboardInterrupt:
        print("\n监控已停止")
    except Exception as e:
        print(f"\n错误: {e}")
    finally:
        ser.close()
        print(f"串口 {port} 已关闭")

def main():
    parser = argparse.ArgumentParser(description='串口数据监控工具')
    parser.add_argument('port', help='串口名称，如 COM3')
    parser.add_argument('-b', '--baudrate', type=int, default=9600,
                       help='波特率 (默认: 9600)')
    parser.add_argument('-t', '--timeout', type=float, default=1.0,
                       help='读取超时秒数 (默认: 1.0)')
    parser.add_argument('--hex', action='store_true',
                       help='显示十六进制数据')
    parser.add_argument('--no-timestamp', action='store_true',
                       help='不显示时间戳')
    parser.add_argument('--no-line-numbers', action='store_true',
                       help='不显示行号')
    
    args = parser.parse_args()
    
    monitor_serial(
        port=args.port,
        baudrate=args.baudrate,
        timeout=args.timeout,
        show_hex=args.hex,
        show_timestamp=not args.no_timestamp,
        show_line_numbers=not args.no_line_numbers
    )

if __name__ == "__main__":
    # 如果没有提供参数，显示帮助并列出可用串口
    if len(sys.argv) == 1:
        try:
            import serial.tools.list_ports
            ports = list(serial.tools.list_ports.comports())
            if ports:
                print("可用串口:")
                for port in ports:
                    print(f"  {port.device}: {port.description}")
                print("\n使用方法:")
                print("  python serial_monitor.py COM3 -b 115200")
                print("  python serial_monitor.py COM3 --hex")
            else:
                print("未找到可用串口")
        except ImportError:
            print("错误: 未找到pyserial库")
            print("请安装: pip install pyserial")
    else:
        main()