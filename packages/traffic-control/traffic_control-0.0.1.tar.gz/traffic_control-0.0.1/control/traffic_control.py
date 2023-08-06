#!/usr/bin/python
# -*- coding: UTF-8 -*-
import paramiko




def init_tc(ip,udpOnlySwitch):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname='10.219.34.20', port=22, username='hih-d-19278', password='123', allow_agent=False,look_for_keys=False)
    if udpOnlySwitch:
        cmd = "./tc_config_udp.py up "+ ip +" 0 0 0 0 200000;./tc_config_udp.py down " + ip +" 0 0 0 0 200000"
    else:
        cmd = "./tc_config.py up " + ip + " 0 0 0 0 200000;./tc_config.py down " + ip + " 0 0 0 0 200000"
    print(type(cmd))
   
    stdin, stdout, stderr = ssh.exec_command(cmd,get_pty=True)
    result = stdout.read()
    print(result.decode())
    ssh.close()
    

def tc(direction, ip, band, delay, jitter, loss, buffer,udpOnlySwitch):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname='10.219.34.20', port=22, username='hih-d-19278', password='123', allow_agent=False,look_for_keys=False)
    if udpOnlySwitch:
        cmd = './tc_config_udp.py ' + direction + ' ' + str(ip) + ' ' + str(band) + ' ' + str(delay) + ' ' + str(
            jitter) + ' ' + str(loss) + ' ' + str(buffer)  # 多个命令用;隔开
    else:
        cmd = './tc_config.py ' + direction + ' ' + str(ip) + ' ' + str(band) + ' ' + str(delay) + ' ' + str(
            jitter) + ' ' + str(loss) + ' ' + str(buffer)  # 多个命令用;隔开
    # cmd = 'python ./tc_config.py up 192.168.2.17 0 0 0 0 1000'
    print(cmd)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read() 
    if not result:
        result = stderr.read()
    ssh.close()
    print(result.decode())
    #cmd = 'cd /home/hih-d-12373;pwd'




if __name__ == '__main__':
    #tc('down','192.168.1.229',0,0,0,0,200000,True)
    init_tc('192.168.1.106',True)
    #init_tc()


