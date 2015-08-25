#!/usr/bin/python
#coding:utf8
import os,sys
def selectServers(selectserver,allserver,HostsGroup):
	selectserver=selectserver.split(',')
	allserver=allserver
	HostsGroup=HostsGroup
	selectserver_back=[]
	for user_and_ip in selectserver:
		ip=user_and_ip.split('@')[1]
		if ip in allserver:selectserver_back.append(ip)#判断算定的是否是一个IP，而不是主机组
	allgroupname=HostsGroup.keys()
	for select_groupname in selectserver:
		if select_groupname in allgroupname:
			selectserver_back.extend(HostsGroup[select_groupname])
	return selectserver_back

		
	
