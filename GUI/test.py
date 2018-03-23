import paramiko
import json
ip='172.16.136.3'
port=2001
username='root'
password='linux'
a=[]
cmd='radosgw-admin user info --uid=test-user' 

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password)

stdin,stdout,stderr=ssh.exec_command(cmd)
outlines=stdout.readlines()
#resp=''.join(outlines)
print(outlines)
encoded_str = json.dumps(outlines)
encoded_str[2]
#resp=resp.split("\"")[1]
#a.append(resp)
#print(a[0])