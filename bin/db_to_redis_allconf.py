#!/usr/bin/env python
#coding:utf-8
import os,sys,json
sys.path.append("/home/cheungssh/mysite")
sys.path.append("/home/cheungssh/mysite/mysite/cheungssh")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from mysite.cheungssh.models import ServerConf
from django.core.cache import cache
def allhostconf():
	allconfinfo={"msgtype":"allconf","content":{}}
        t_allconfinfo=cache.get("allconf")
        if t_allconfinfo is None:
                data=ServerConf.objects.all()
                for a in data:
                        t_host={}
                        t_host["id"]=a.id
			t_host["su"]=a.Su
			t_host["supassword"]=a.SuPassword
                        t_host["group"]=a.Group
                        t_host["ip"]=a.IP
                        t_host["username"]=a.Username
                        t_host["password"]=a.Password
                        t_host["hostname"]=a.HostName
                        t_host["port"]=int(a.Port)
                        t_host["keyfile"]=a.KeyFile
                        t_host["sudo"]=a.Sudo
                        t_host["su"]=a.Su
                        t_host["supassword"]=a.SuPassword
                        t_host["loginmethod"]=a.LoginMethod
			allconfinfo['content'][a.id]=t_host
        		cache.set("allconf",allconfinfo,360000)
        else:
                allconfinfo=t_allconfinfo
	return allconfinfo
