#/usr/bin/python
#coding:utf8
import paramiko,os
def UpdateFile(ip,port,username,password,UseKey,sfile,dfile):
	try:
		t=paramiko.Transport((ip,port))
		if UseKey=="Y":
			KeyPath=os.path.expanduser('~/.ssh/id_rsa')
			key=paramiko.RSAKey.from_private_key_file(KeyPath)
			t.connect(username = username,pkey=key)
		else:
			t.connect(username = username,password = password)
		sftp = paramiko.SFTPClient.from_transport(t)
		ret=sftp.put(sfile,dfile)
		
	except Exception,e:
		print "-Error 不能更新服务器上[%s]的文件(%s)"% (ip,e)
		return False
	else:
		t.close()
		print "+Update File is OK [%s]"%ip
		return True
