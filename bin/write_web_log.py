#!/usr/bin/python
#coding:utf-8
import os,sys
HOME=os.path.join(os.environ["HOME"],'cheung')
LogFile=os.path.join(HOME,"logs/web_run.log")
def write_web_log(info):
	try:
		a=open(LogFile,"a")
		a.write(info+"\n")
	except Exception,e:
		return "不能写入日志",e

