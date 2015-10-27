#!/usr/bin/python
#coding:utf8
#Author=Cheung Kei-Chuen
#QQ=2418731289 
VERSION=131
import socket,os,sys,db_to_redis_allconf,cheungssh_su,cheungssh_sudo
socket.setdefaulttimeout(3)
sys.path.append("/home/cheungssh/mysite/mysite/cheungssh/")
import paramiko,threading,time,commands,re,Format_Char_Show_web,shutil,random,json,sendinfo,key_resolv
from mysite.cheungssh.models import ServerConf
from django.core.cache import cache
def SSH_cmd(ip,username,password,port,loginmethod,keyfile,cmd,ie_key,group,Data):
	PROFILE=". /etc/profile 2&>/dev/null;. ~/.bash_profile 2&>/dev/null;. /etc/bashrc 2&>/dev/null;. ~/.bashrc 2&>/dev/null;"
	PATH="export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin;"
	start_time=time.time()
	ResultSum=''
	ResultSumLog=''
	color_status=0
	try:
		o=None
		err=None
		ssh=paramiko.SSHClient()
		if loginmethod=='KEY':
	
			KeyPath=keyfile
			key=paramiko.RSAKey.from_private_key_file(KeyPath)
			ssh.load_system_host_keys()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,port,username,pkey=key)  
		else:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,int(port),username,password)
		stdin,stdout,stderr=ssh.exec_command(PROFILE+PATH+cmd)
		out=stdout.readlines()
		Data.All_Servers_num += 1
		for o in out:
			ResultSum +=o
			ResultSumLog +=o.strip('\n') + '\\n'
		
		error_out=stderr.readlines()
		for err in error_out:
			ResultSum +=err
			ResultSumLog +=err.strip('\n') + '\\n'
		if err:
			Data.FailIP.append(ip)
			color_status=1
			ResultSum_count="服务器: %s@%s  错误消息: %s" %(username,ip,"命令失败")
			out='Null\n'
		else:
			error_out='NULL'
			ResultSum_count="服务器: %s@%s " %(username,ip)
			Data.All_Servers_num_Succ+=1
		Show_Result_web_status=Format_Char_Show_web.Show_Char(ResultSum.replace("<","&lt;")+username+"@"+ip,color_status)
		Show_Result=ResultSum + '\n' +ResultSum_count
		jindu=int(float(Data.All_Servers_num)/float(Data.All_Servers_num_all)*100)
		TmpShow=Format_Char_Show_web.Show_Char(Show_Result+" 命令: "+cmd,color_status)  
		if color_status==1:
			info={"msgtype":1,"content":[{"group":group,"servers":[{"ip":username+"@"+ip,"status":"ERR","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		else:
			info={"msgtype":1,"content":[{"group":group,"servers":[{"ip":username+"@"+ip,"status":"OK","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		b_id=str(random.randint(999999999,99999999999999999))
		info["id"]=b_id
		info=json.dumps(info,encoding='utf8',ensure_ascii=False)
	except Exception,e:
		print e
		ResultSum=str(e)
		color_status=1
		Data.FailIP.append(ip)
		Data.All_Servers_num += 1
		ResultSum_count="服务器: %s@%s  错误消息: %s" %(username,ip,e)
		Show_Result_web_status=ResultSum 
		Show_Result= ResultSum+ResultSum_count

                TmpShow=Format_Char_Show_web.Show_Char(Show_Result+" 命令: "+cmd,color_status)
		jindu=int(float(Data.All_Servers_num)/float(Data.All_Servers_num_all)*100)
		Show_Result_web_status=Format_Char_Show_web.Show_Char(str(e).replace("<","&lt;")+"\n"+username+"@"+ip,color_status)
		info={"msgtype":1,"content":[{"group":group,"servers":[{"ip":username+"@"+ip,"status":"ERR","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		info['id']=(str(random.randint(999999999,99999999999999999)))
		info=json.dumps(info,encoding='utf8',ensure_ascii=False)
	else:
		ssh.close()
	#sendinfo.sendinfo(str({ie_key:info}))
	######### 硬件检测
	if Data.excutetype=='cmd':
		sendinfo.sendinfo(str({ie_key:info}))
	elif Data.excutetype=='crontab':
		# logline的数据格式是 key ：['status', 'runtime', 'user', 'fid', 'runtype', 'ip', 'cmd', 'id', 'createtime']
		#计划任务命令存储数据格式: { fid :  {}  }
		crondlog_show=cache.get('crondlog')
		if  crondlog_show:
			lasttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
			crondlog_show[Data.fid]['content']=ResultSum
			crondlog_show[Data.fid]['lasttime']=lasttime
			if color_status==0:
				crondlog_show[Data.fid]['status']="正常"
			else:
				crondlog_show[Data.fid]['status']="失败"
			cache.set('crondlog',crondlog_show,8640000000)
			print "已经写入"
		else:
			print "没有crond记录， 则不写"
			pass
		pass
	else:
		checktime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		ipinfo={Data.hwtype:ResultSum,'ip':ip,'checktime':checktime}
		hwinfo=cache.get('hwinfo')
		if not  hwinfo:
			hwinfo={ip:ipinfo}
		else:	
			if not  hwinfo.has_key(ip):
				hwinfo[ip]=ipinfo
		hwinfo[ip][Data.hwtype]=ResultSum
		hwinfo[ip]['checktime']=checktime
		cache.set('hwinfo',hwinfo,864000000)
	#########
def main(cmd,ie_key,selectserver,Data,excutetype='cmd',hwtype='CPU'):
	Data.excutetype=excutetype
	Data.hwtype=hwtype
	Data.FailIP=[]
	Data.All_Servers_num_all=0
	Data.All_Servers_num=0
	Data.All_Servers_num_Succ=0
	Data.i=0
	all_conf=db_to_redis_allconf.allhostconf()['content']
	Data.conf=all_conf
	if selectserver=='all':
		selectserver=Data.conf.keys()
	else:
		selectserver=selectserver.split(',')
	print selectserver
	Data.All_Servers_num_all=len(selectserver)
	Data.i=len(selectserver)
	for id in selectserver:
		if Data.conf[id]['loginmethod']=='KEY':
			keyfile=key_resolv.key_resolv(Data.conf[id]["keyfile"],cache)
		else:
			keyfile='N'
		if Data.conf[id]["su"]=="Y" and excutetype=='cmd' :
			b=threading.Thread(target=cheungssh_su.Excute_suroot,args=(Data.conf[id]["ip"],Data.conf[id]["username"],Data.conf[id]["password"],Data.conf[id]["port"],Data.conf[id]["loginmethod"],keyfile,cmd,ie_key,Data.conf[id]["group"],Data.conf[id]["supassword"],Data))
		elif Data.conf[id]["sudo"]=="Y" and excutetype=='cmd':
			b=threading.Thread(target=cheungssh_sudo.Excute_sudo,args=(Data.conf[id]["ip"],Data.conf[id]["username"],Data.conf[id]["password"],Data.conf[id]["port"],Data.conf[id]["loginmethod"],keyfile,cmd,ie_key,Data.conf[id]["group"],Data.conf[id]["password"],Data))
		else:
			b=threading.Thread(target=SSH_cmd,args=(Data.conf[id]["ip"],Data.conf[id]["username"],Data.conf[id]["password"],Data.conf[id]["port"],Data.conf[id]["loginmethod"],keyfile,cmd,ie_key,Data.conf[id]["group"],Data))
		b.start()
	b.join()
if __name__=='__main__':
	from DataConf import DataConf
	Data=DataConf()
	fid=sys.argv[1]
	Data.fid=fid
	cmdfile="/home/cheungssh/data/cmd/cmdfile"
	fcontent=open(cmdfile)
	cmd=''
	selectserver=''
	for a in fcontent:
		cmdline=a.strip().split('#')
		if cmdline[-1]==fid:
			cmd ="#".join(cmdline[0:-2])  #命令 服务器 fid 
			selectserver=cmdline[-2]
			fcontent.close()
			break
	print cmd
	main(cmd,'all-ie',selectserver,Data,'crontab')
