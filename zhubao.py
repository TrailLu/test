# from scapy.all import *
# # 抓3个包
# packets = sniff(count=3)
# packets.summary()

# # 构造并发送 ping 包
# send(IP(dst="8.8.8.8")/ICMP())


# import paramiko
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('10.0.2.15', username='liu0071', password='liushiyuan')
# stdin, stdout, stderr = ssh.exec_command('ls -la')
# print(stdout.read().decode())
# ssh.close()

import paramiko

hostname = '192.168.0.11'
username = 'Liu0071'
password = '200001'

# 要执行的 bash 命令
command = 'journalctl -n 100 > ~/logs.txt'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)

stdin, stdout, stderr = ssh.exec_command(command)
print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
