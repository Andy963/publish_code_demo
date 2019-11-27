from django.test import TestCase
import paramiko
# Create your tests here.
ssh = paramiko.SSHClient()

#允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接服务器
ssh.connect(hostname='127.0.0.1', port=2222, username='root',password='zjgisadmin')

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df -h')

# 获取命令结果
result = stdout.read()

# 关闭连接
ssh.close()

print(result.decode('utf-8'))