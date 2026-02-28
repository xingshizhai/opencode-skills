#!/usr/bin/env python3
"""
向串口发送命令并接收响应
支持交互模式、单次命令和文件批量发送
"""

import serial
import argparse
import sys
import time

class SerialCommunicator:
    def __init__(self, port, baudrate=9600, timeout=1, write_timeout=1):
        """初始化串口通信器
        
        Args:
            port: 串口名称
            baudrate: 波特率
            timeout: 读取超时
            write_timeout: 写入超时
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.ser = None
        
    def open(self):
        """打开串口"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                write_timeout=self.write_timeout
            )
            print(f"串口 {self.port} 已打开 ({self.baudrate} baud)")
            return True
        except serial.SerialException as e:
            print(f"无法打开串口 {self.port}: {e}")
            return False
    
    def close(self):
        """关闭串口"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"串口 {self.port} 已关闭")
    
    def send_command(self, command, wait_response=True, response_timeout=None):
        """发送命令并接收响应
        
        Args:
            command: 命令字符串或字节
            wait_response: 是否等待响应
            response_timeout: 响应超时时间，None使用默认timeout
        
        Returns:
            响应数据（字节）或None
        """
        if not self.ser or not self.ser.is_open:
            print("错误: 串口未打开")
            return None
        
        # 转换为字节
        if isinstance(command, str):
            command_bytes = command.encode('utf-8')
        else:
            command_bytes = command
        
        # 发送命令
        print(f"发送: {command_bytes!r}")
        try:
            self.ser.write(command_bytes)
            self.ser.flush()
        except serial.SerialTimeoutException:
            print("错误: 写入超时")
            return None
        
        # 等待响应
        if wait_response:
            timeout = response_timeout if response_timeout is not None else self.timeout
            start_time = time.time()
            response = bytearray()
            
            while True:
                if timeout and (time.time() - start_time) > timeout:
                    break
                
                if self.ser.in_waiting:
                    data = self.ser.read(self.ser.in_waiting)
                    response.extend(data)
                    start_time = time.time()  # 收到数据后重置超时
                elif response:  # 已有数据且当前无新数据
                    time.sleep(0.01)
                else:
                    time.sleep(0.01)
            
            if response:
                print(f"接收: {bytes(response)!r}")
                # 尝试解码为文本
                try:
                    text = bytes(response).decode('utf-8', errors='replace')
                    print(f"文本: {text}")
                except:
                    pass
                # 显示十六进制
                hex_str = ' '.join(f'{b:02X}' for b in response)
                print(f"十六进制: {hex_str}")
                return bytes(response)
            else:
                print("未收到响应")
                return None
        else:
            return None
    
    def interactive_mode(self):
        """交互式模式"""
        print("\n进入交互模式 (输入 'quit' 或 'exit' 退出)")
        print("命令格式:")
        print("  text: 文本命令 (自动转换为字节)")
        print("  hex: 十六进制命令 (如 41 42 43 表示 ABC)")
        print("  raw: 原始字节 (如 b'Hello')")
        print()
        
        while True:
            try:
                user_input = input(">>> ").strip()
                
                if user_input.lower() in ('quit', 'exit', 'q'):
                    break
                elif not user_input:
                    continue
                elif user_input.startswith('hex '):
                    # 十六进制命令
                    hex_str = user_input[4:].strip()
                    try:
                        hex_bytes = bytes.fromhex(hex_str)
                        self.send_command(hex_bytes)
                    except ValueError:
                        print("错误: 无效的十六进制格式")
                elif user_input.startswith('raw '):
                    # 原始字节命令
                    raw_cmd = user_input[4:].strip()
                    try:
                        # 使用eval解析字节字符串
                        cmd_bytes = eval(raw_cmd)
                        if isinstance(cmd_bytes, bytes):
                            self.send_command(cmd_bytes)
                        else:
                            print("错误: 必须是字节字符串，如 b'Hello'")
                    except:
                        print("错误: 无法解析字节字符串")
                else:
                    # 文本命令
                    self.send_command(user_input)
                    
            except KeyboardInterrupt:
                print("\n退出交互模式")
                break
            except Exception as e:
                print(f"错误: {e}")

def main():
    parser = argparse.ArgumentParser(description='串口命令发送工具')
    parser.add_argument('port', help='串口名称，如 COM3')
    parser.add_argument('-b', '--baudrate', type=int, default=9600,
                       help='波特率 (默认: 9600)')
    parser.add_argument('-c', '--command', help='要发送的命令（文本）')
    parser.add_argument('--hex', help='要发送的十六进制命令')
    parser.add_argument('-f', '--file', help='从文件读取命令（每行一个命令）')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='进入交互模式')
    parser.add_argument('--no-response', action='store_true',
                       help='不等待响应')
    parser.add_argument('-t', '--timeout', type=float, default=1.0,
                       help='响应超时秒数 (默认: 1.0)')
    
    args = parser.parse_args()
    
    # 创建通信器
    comm = SerialCommunicator(
        port=args.port,
        baudrate=args.baudrate,
        timeout=args.timeout
    )
    
    if not comm.open():
        return 1
    
    try:
        # 交互模式
        if args.interactive:
            comm.interactive_mode()
        
        # 从文件发送命令
        elif args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        cmd = line.strip()
                        if cmd and not cmd.startswith('#'):  # 跳过空行和注释
                            print(f"\n命令 #{line_num}: {cmd}")
                            comm.send_command(cmd, not args.no_response)
                            time.sleep(0.1)  # 命令间短暂延迟
            except FileNotFoundError:
                print(f"错误: 文件未找到 {args.file}")
        
        # 发送十六进制命令
        elif args.hex:
            try:
                hex_bytes = bytes.fromhex(args.hex)
                comm.send_command(hex_bytes, not args.no_response)
            except ValueError:
                print("错误: 无效的十六进制格式")
        
        # 发送文本命令
        elif args.command:
            comm.send_command(args.command, not args.no_response)
        
        # 如果没有指定任何模式，显示帮助
        elif not args.interactive and not args.file and not args.hex and not args.command:
            print("未指定命令模式，使用以下选项之一:")
            print("  -i, --interactive   进入交互模式")
            print("  -c COMMAND          发送文本命令")
            print("  --hex HEX_CMD       发送十六进制命令")
            print("  -f FILE             从文件读取命令")
            print("\n示例:")
            print(f"  python send_command.py {args.port} -b 115200 -i")
            print(f"  python send_command.py {args.port} -c \"AT\\r\\n\"")
            print(f"  python send_command.py {args.port} --hex \"41 54 0D 0A\"")
    
    finally:
        comm.close()
    
    return 0

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
                print("  python send_command.py COM3 -i")
                print("  python send_command.py COM3 -c \"AT\"")
            else:
                print("未找到可用串口")
        except ImportError:
            print("错误: 未找到pyserial库")
            print("请安装: pip install pyserial")
    else:
        sys.exit(main())