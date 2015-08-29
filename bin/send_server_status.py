#!/usr/bin/python
#coding:utf8
import os,sys
reload(sys)
sys.setdefaultencoding("utf-8")
def send_status():
	server_status={"10.0.0.1":"red","10.0.0.2":"green","10.0.0.3":"red"}
	server_info={"10.0.0.1":"服务器:root@10.0.0.1 </br>消息:服务器没响应"}
	return server_status,server_info
if  __name__=='__main__':
	print send_status()
