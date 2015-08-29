#/usr/bin/python
#coding:utf8
import paramiko,os
def GetFile(ip,port,username,password,UseKey,sfile,dfile):
	dfile='/tmp/'+os.path.basename(dfile)
	try:
		t=paramiko.Transport((ip,port))
		if UseKey=="Y":
			KeyPath=os.path.expanduser('~/.ssh/id_rsa')
			key=paramiko.RSAKey.from_private_key_file(KeyPath)
			t.connect(username = username,pkey=key)
		else:
			t.connect(username = username,password = password)
		sftp = paramiko.SFTPClient.from_transport(t)
		ret=sftp.get(sfile,dfile)
		
	except Exception,e:
		print "不能获取获取远程服务器上的文件(%s)"%e
		return False
	else:
		t.close()
		print "+Get File is OK"
		return True
