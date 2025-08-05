import socket

# 创建 socket 对象
s = socket.socket()

# 绑定到本地地址和端口0.0.0.0
#代表服务器监听所有 IP
#（外网内网都可以连）
s.bind(('0.0.0.0', 12345))

# 开始监听
s.listen(1)

# 等待客户端连接
conn, addr = s.accept()

print("Connected by", addr)

# 接收客户端发来的数据
data = conn.recv(1024)
print("Received:", data.decode())

# 给客户端回复消息
conn.send(b'Hello from server')
