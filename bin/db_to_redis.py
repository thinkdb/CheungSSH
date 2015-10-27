#!/usr/bin/evn python
#coding:utf-8
import json
import os,sys
sys.path.append("/home/cheungssh/mysite")
sys.path.append("/home/cheungssh/mysite/mysite/cheungssh")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from mysite.cheungssh.models import ServerConf
from django.core.cache import cache
def db_to_redis(id):
	Data=ServerConf.objects.all()
 	hostinfo={"msgtype":"host","content":[]}
	for a in Data:
		if not str(a.id)==str(id):
			continue
		t_host={
			"id":a.id,
			"ip":a.IP,
			"group":a.Group,
			"port":a.Port,
			"username":a.Username,
			"password":a.Password,
			#"keyfile":a.KeyFile.path,  #这个是文件控件， 要用path访问，否则报错
			"keyfile":a.KeyFile,  #这个是文件控件， 要用path访问，否则报错
			"sudo":a.Sudo,
			"sudopassword":a.SudoPassword,
			"su":a.Su,
			"supassword":a.SuPassword,
			"loginmethod":a.LoginMethod,
			}
		try:
			cache.set("host:%s"% (a.id),t_host,3600000)
			return t_host
		except Exception,e:
			return False
	#"no-id"
	return False
	
	
