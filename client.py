import socket

# 创建 socket 对象
s = socket.socket()

# 连接到服务器 代表本机（只能自己连自己）
s.connect(('127.0.0.1', 12345))

# 向服务器发送数据
s.send(b'Hello from client')

# 接收服务器的回复
print(s.recv(1024).decode())
