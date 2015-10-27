#!/usr/bin/env python
#coding:utf-8
import os,sys,random
from cheunglog import log
model="daemon-transfile"
sys.path.append('/home/cheungssh/mysite')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from mysite.cheungssh.FileTransfer import getconf
if __name__  == '__main__':
	#'{"sfile":"/tmp/abc","dfile":"/tmp/cbd","id":"1","user":"haha","runtype":"upload","fid":111111111111111111}' 
	host = " ".join(sys.argv[1:])
	try:
		host=eval(host)
		if not type({})==type(host):
			log(model,"参数类型不是dict")
			sys.exit(1)
		else:
			log(model,"started")
			if host.has_key('fid'):
				fid=host['fid']
			else:
				fid=str(random.randint(90000000000000000000,99999999999999999999))
			try:
				getconf(host,fid,host["user"],host["runtype"])
			except Exception,e:
				log(model,str(e))
			
	except Exception,e:
		print e
		msg=str(e)
		log(model,msg)
		sys.exit(1)
