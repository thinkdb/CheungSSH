#!/usr/bin/evn python
#coding:utf-8
import os,json,sys,commands,cheungssh_web,DataConf
#Data=DataConf.DataConf()
def collect(id='all'):
	cmd={
	"platform":"/usr/sbin/dmidecode -s system-product-name|tail -1",
	"os":"""awk  'NR==1{print}'  /etc/issue""",
	"bit":"getconf LONG_BIT",
	"cpu_num":"grep 'physical id' /proc/cpuinfo| sort| uniq| wc -l",
	"core_num":"""grep "processor" /proc/cpuinfo| wc -l""",
	"cpu_type":"""grep name  /proc/cpuinfo| cut -f2 -d: | uniq -c""",
	"serial_num":"""/usr/sbin/dmidecode  -s  system-serial-number|sed 's/ //g'""",
	"interface":"""lspci|grep 'Ethernet'""",
	"mem":"""/usr/bin/free -m|awk  '$1=="Mem:"{printf("%sMB",$2)}'""",
	"disk":"""parted -l | grep -E  '^Disk' | grep -v mapper""",
	"mac":"""/sbin/ifconfig -a |awk  '$0~/HWaddr/{print $NF}'""",
	"hostname":"hostname",
	"swap":"""/usr/bin/free -m|awk  '$1=="Swap:"{printf("%sMB",$2)}'"""}
	for a in cmd.keys():
		Data=DataConf.DataConf()
		cheungssh_web.main(cmd[a],'all-ie',id,Data,'hardware',a)
if __name__=='__main__':
	collect()
