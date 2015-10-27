#!/usr/bin/python
#coding:utf-8
import os,sys,time
LogFile="/home/cheungssh/logs/run.log"
nowtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
def log(model="web",info="Null"):
	info=str(nowtime) + " " + str(model) + " "  + info+"\n"
	try:
		t=open(LogFile,'a')
		t.write(info)
		t.close()
	except Exception,e:
		pass
		
	
