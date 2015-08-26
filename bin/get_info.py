#!/usr/bin/python
#coding:utf8
import os,sys,commands,json,sendinfo
HOME=os.path.expanduser("~")
os.sys.path.insert(0,"%s/cheung/bin"%HOME)
import cheungssh_web,sendinfo
server_info=cheungssh_web.Read_config()
reload(sys)
sys.setdefaultencoding('utf8')
import random
def get_info(msgtype=1):
	info={"msgtype":msgtype,"content":[]}
	for ip in server_info[-1]:
		for g in server_info[2]:
			if ip in server_info[2][g]:
				InGroup=g
				info_tmp={"group":InGroup,"servers":[{"ip":server_info[0][ip]+"@"+ip,"status":"UNSTART","jindu":0,"info":"尚未启动"}]}
				
				i=0
				isInGroup=False
				for a in info["content"]:
					try:
						if InGroup==info["content"][i]["group"]:
							isInGroup=True
							info["content"][i]["servers"].append({"status:":"UNSTART","ip":server_info[0][ip]+"@"+ip,"jindu":0,"info":"尚未启动"})
							break
						else:
							i+=1
							continue
					except Exceptoin,e:
						i+=1
						continue
				if not isInGroup:
					info["content"].append(info_tmp)
				break
	info=json.dumps(info,encoding='utf8',ensure_ascii=False)
	return str(info)
if __name__=='__main__':
	print str(get_info())
	commands.getstatusoutput("yes|cp  -f %s/cheung/data/server_info{,.TMP}" %HOME)

