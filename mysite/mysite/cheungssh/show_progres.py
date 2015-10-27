#/usr/bin/python
#coding:utf8
import paramiko,os,sys
def show_progres(transferred, toBeTransferred,id=1111):
	allsize=toBeTransferred
	nowsize=transferred
	logfile="/tmp/.cheungssh_file_trans.tmp"
	progres="%d" % (float(nowsize)/float(allsize)*100)
	try:
		cmd="""sed -i "/^%s,/d" %s""" % (id,logfile)
		os.system(cmd)
		t=open(logfile,"a")
		msg=str(id)+ str(",") + str(progres)
		t.write(msg+"\n")
	except Exception,e:
		print e
		pass
	t.close()
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
		ret=sftp.get(sfile,dfile,callback=show_progres(**,**,11111))
		
	except Exception,e:
		print "不能获取获取远程服务器上的文件(%s)"%e
		return False
	else:
		t.close()
		print "+Get File is OK"
		return True
