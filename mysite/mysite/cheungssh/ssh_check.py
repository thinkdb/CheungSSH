#!/usr/bin/evn python
#coding:utf8
#张其川


def ssh_check(conf):
	username=conf['username']
	password=conf['password']
	port=conf['port']
	ip=conf['ip']
	loginmethod=conf['loginmethod']
	info={"msgtype":"ERR","content":""}
	try:
		import paramiko
		ssh=paramiko.SSHClient()
		if loginmethod=='KEY':
			KeyPath=conf['keyfile']
			key=paramiko.RSAKey.from_private_key_file(KeyPath)
			ssh.load_system_host_keys()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,port,username,pkey=key)  
                else:
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(ip,int(port),username,password)
		info['msgtype']="OK"
		ssh.close()
	except Exception,e:
		info['content']=str(e)
	return info
		
	
	
