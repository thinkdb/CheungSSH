#!/usr/bin/python
#coding:utf8
#Author=Cheung Kei-Chuen
#QQ=2418731289
VERSION=130
import os,sys
import commands
HOME=os.path.expanduser('~')
import sendinfo
os.sys.path.insert(0,os.path.abspath('./'))
os.sys.path.insert(0,os.path.abspath('%s/cheung/bin/'%HOME))
try:
	import paramiko,threading,socket,ConfigParser,time,commands,threading,re,getpass,Format_Char_Show_web,shutil,random,getpass,LogCollect,readline,filemd5,GetFile,UpdateFile,json,sendinfo,selectHosts
except Exception,e:
	print "\033[1m\033[1;31m-ERR %s\033[0m\a"	% (e)
	sys.exit(1)
reload(sys)
SysVersion=float(sys.version[:3])
sys.setdefaultencoding('utf8')
LogFile='%s/cheung/logs/cheungssh.log' %HOME
SLogFile='%s/cheung/logs/cheungssh.source.log' %HOME
DeploymentFlag="/tmp/DeploymentFlag%s" % (str(random.randint(999999999,999999999999)))
HostsFile="%s/cheung/conf/hosts" %HOME
ConfFile="%s/cheung/conf/cheung.conf" %HOME
try:
	paramiko.util.log_to_file('%s/cheung/logs/paramiko.log' %HOME)
except Exception,e:
	pass
T_V=sys.version.split()[0]
if int(T_V.replace(".","")) <240:
	print "Python's version can not less than 2.4"
	print "Please : yum  update  -y  python"
	sys.exit(1)
def write_msg(info):
	global dir_i
	try:
		dir=open("%s/cheung/data/dir"%HOME).readline().strip()
		os.system("""mkdir  -p %s/cheung/data/msg%s"""%(HOME,dir))
		a=open("%s/cheung/data/msg%s/%s"%(HOME,dir,dir_i),"w")
		a.write(info)
		a.close()
		dir_i+=1
	except Exception,e:
		print "不能写入消息",e
def write_server_status(info):
	global cmd_status_dir_i
	try:
		cmd_server_dir=open("%s/cheung/data/dir"%HOME).readline().strip()
		os.system("""mkdir  -p %s/cheung/data/status%s"""%(HOME,cmd_server_dir))
		a=open("%s/cheung/data/status%s/%s"%(HOME,cmd_server_dir,cmd_status_dir_i),"w")
		a.write(info)
		a.close()
		cmd_status_dir_i+=1
	except Exception,e:
		print "不能写入状态",e
def SSH_cmd(ip,username,password,port,cmd,UseLocalScript,OPTime,ie_key):
	PROFILE=". /etc/profile 2&>/dev/null;. ~/.bash_profile 2&>/dev/null;. /etc/bashrc 2&>/dev/null;. ~/.bashrc 2&>/dev/null;"
	PATH="export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin;"
	global All_Servers_num,All_Servers_num_all,All_Servers_num_Succ,Done_Status,Global_start_time,PWD,FailIP,Servers
	start_time=time.time()
	ResultSum=''
	ResultSumLog=''
	DeploymentStatus=False
	DeploymentInfo=None
	color_status=0
	InGroup=""
	for a in HostsGroup:
		if ip in HostsGroup[a]:
			InGroup=a
			break
			
	try:
		o=None
		err=None
		ssh=paramiko.SSHClient()
		if UseKey=='Y':
	
			KeyPath=os.path.expanduser('~/.ssh/id_rsa')
			key=paramiko.RSAKey.from_private_key_file(KeyPath)
			ssh.load_system_host_keys()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,port,username,pkey=key)  
		else:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,port,username,password)
		stdin,stdout,stderr=ssh.exec_command(PROFILE+PATH+cmd)
		out=stdout.readlines()
		All_Servers_num += 1
		print "\r"
		for o in out:
			ResultSum +=o
			ResultSumLog +=o.strip('\n') + '\\n'
		
		error_out=stderr.readlines()
		for err in error_out:
			ResultSum +=err
			ResultSumLog +=err.strip('\n') + '\\n'
		if err:
			FailIP.append(ip)
			color_status=1
			ResultSum_count="服务器: %s@%s  错误消息: %s" %(username,ip,"命令失败")
			out='Null\n'
		else:
			error_out='NULL'
			#ResultSum_count="\033[1m\033[1;32m+OK [%s|%s] (%0.2f Sec, %d/%d  Cmd:Sucess)\033[1m\033[0m" % (ip,username,float(time.time()-start_time),All_Servers_num,All_Servers_num_all)
			ResultSum_count="服务器: %s@%s " %(username,ip)
			All_Servers_num_Succ+=1
		Show_Result_web_status=Format_Char_Show_web.Show_Char(ResultSum.replace("<","&lt;")+username+"@"+ip,color_status)
		Show_Result=ResultSum + '\n' +ResultSum_count
		#jindu=("%0.2f" %(All_Servers_num/All_Servers_num_all))*100
		jindu=int(float(All_Servers_num)/float(All_Servers_num_all)*100)
		TmpShow=Format_Char_Show_web.Show_Char(Show_Result+" 时间:"+OPTime+" 命令: "+cmd,color_status)  
		#write_msg(TmpShow)
		#sendinfo.sendinfo(str({ie_key:TmpShow}))
		if color_status==1:
			info={"msgtype":1,"content":[{"group":InGroup,"servers":[{"ip":username+"@"+ip,"status":"ERR","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		else:
			info={"msgtype":1,"content":[{"group":InGroup,"servers":[{"ip":username+"@"+ip,"status":"OK","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		b_id=str(random.randint(999999999,99999999999999999))
		info["id"]=b_id
		info=json.dumps(info,encoding='utf8',ensure_ascii=False)
		sendinfo.sendinfo(str({ie_key:info}))
		#serverinfo={InGroup:[ip:{"status":"OK","info":Show_Result}]}
		#serverinfo=[1,{InGroup:[{ip:{"ip":username+"@"+ip,"status":"OK","info":Show_Result}}]}]
		#serverinfo={ip:{"status":"UNSTART","groupid":InGroup,"ip":server_info[0][ip]+"@"+ip,"info":"暂无消息"}}
		#serverinfo=str(serverinfo).decode('latin-1').encode("utf-8")
		#serverinfo=json.dumps(serverinfo,encoding='utf8',ensure_ascii=False)
		#write_server_status("IP_Status===%s===%s===ok===消息:%s===/pic/green.png"%(InGroup,ip,Show_Result))
		#write_server_status(str(serverinfo))
	except Exception,e:
		color_status=1
		FailIP.append(ip)
		All_Servers_num += 1
		#ResultSum_count="\n\033[1m\033[1;31m-ERR [%s|%s] %s (%0.2f Sec %d/%d)\033[1m\033[0m\a"	% (ip,username,e,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
		ResultSum_count="服务器: %s@%s  错误消息: %s" %(username,ip,e)
		Show_Result_web_status=ResultSum 
		Show_Result= ResultSum+ResultSum_count

                TmpShow=Format_Char_Show_web.Show_Char(Show_Result+" 时间:"+OPTime+" 命令: "+cmd,color_status)
		#write_msg(TmpShow)
		jindu=int(float(All_Servers_num)/float(All_Servers_num_all)*100)
		#sendinfo.sendinfo(str({ie_key:TmpShow}))
		Show_Result_web_status=Format_Char_Show_web.Show_Char(str(e).replace("<","&lt;")+"\n"+username+"@"+ip,color_status)
		info={"msgtype":1,"content":[{"group":InGroup,"servers":[{"ip":username+"@"+ip,"status":"ERR","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		info['id']=(str(random.randint(999999999,99999999999999999)))
		info=json.dumps(info,encoding='utf8',ensure_ascii=False)
		sendinfo.sendinfo(str({ie_key:info}))
		#serverinfo=[1,{InGroup:[{ip:{"ip":username+"@"+ip,"status":"ERR","info":Show_Result}}]}]
		#serverinfo=str(serverinfo).decode('latin-1').encode("utf-8")
		#serverinfo=json.dumps(serverinfo,encoding='utf8',ensure_ascii=False)
		#write_server_status(str(serverinfo))
	else:
		ssh.close()
	if All_Servers_num == All_Servers_num_all: #这里防止计数器永远相加下去
		FailNum=All_Servers_num_all-All_Servers_num_Succ
		if FailNum>0:
			FailNumShow="\033[1m\033[1;31mFail:%d\033[1m\033[0m" % (FailNum)
		else:
			FailNumShow="Fail:%d" % (FailNum)
		#print "+Done (Succ:%d,%s, %0.2fSec CheungSSH(V:%d) Cheung Kei-Chuen All Right Reserved)" % (All_Servers_num_Succ,FailNumShow,time.time()-Global_start_time,VERSION)
		All_Servers_num =0
		All_Servers_num_Succ=0
		Done_Status='end'
		#os.system("""echo 'Done' >/tmp/status""")
		sendinfo.sendinfo(str({ie_key:'Done'}))

def Read_config(file="%s/cheung/conf/cheung.conf"%HOME):
	global Servers,Useroot,Timeout,RunMode,UseKey,Deployment,ListenTime,ListenFile,ListenChar,ServersPort,ServersPassword,ServersUsername,ServersRootPassword,NoPassword,NoRootPassword,HostsGroup,HOSTSMD5,CONFMD5,sudo
	ServersPort={};ServersPassword={};ServersUsername={};ServersRootPassword={};Servers=[];HostsGroup={}
	try:
		HOSTSMD5=filemd5.main(HostsFile)
		CONFMD5=filemd5.main(ConfFile)
	except Exception,e:
		print "读取配置文件错误(%s)" % e
		sys.exit(1)
	c=ConfigParser.ConfigParser()
	try:
		c.read(file)
	except ConfigParser.ParsingError,e:
		print "文件%s格式错误.\a\n\t" % (file)
		sys.exit(1)
	except Exception,e:
		print e
		sys.exit(1)
	
	try:
		RunMode=c.get("CheungSSH","RunMode").upper()
	except Exception,e:
		RunMode='M'
		print "No Runmode default Mutiple(M)"
	try:
		UseKey=c.get("CheungSSH","UseKey").upper()
	except:
		UseKey="N"
	try:
		sudo=c.get("CheungSSH","sudo")
	except:
		sudo=False
	try:
		T=open(HostsFile)
		NoPassword=False
		NoRootPassword=False
		OneFlag=True
		for b in T:
			if re.search("^#",b) or re.search("^ *$",b):
				continue
			if re.search("^ *\[.*\] *$",b):
				CurGroup=re.sub("^ *\[|\] *$","",b).strip().lower()
				HostsGroup[CurGroup]=[]
				OneFlag=False
				continue
			else:
				if OneFlag:
					print "请为hosts文件第一行处命令一个主机组的名字 [主机组名字]"
					sys.exit()
			a=b.strip().split("===")
			ServersPort[a[0]]=int(a[1])
			Servers.append(a[0])
			try:
				HostsGroup[CurGroup].append(a[0])
			except Exception,e:
				HostsGroup[CurGroup]=[]
				HostsGroup[CurGroup].append(a[0].lower())
			if UseKey.upper()=="N":
				if len(a)<5:
					print """您的配置文件中没有足够的列:\033[1m\033[1;31m[%s]\033[1m\033[0m\a
请使用如下格式:
主机地址===端口号===登陆账户===登陆密码===su-root密码，如果没有配置使用su-root，此列可为None""" % b.strip()
					sys.exit()
				ServersUsername[a[0]]=a[2]
				TP=re.search("^[Nn][Oo][Nn][Ee]$",a[3])
				if TP:
					
					ServersPassword[a[0]]=None
					NoPassword=True
				else:
					ServersPassword[a[0]]=a[3]
						
			else:
				if len(a)<5:
					print """您的配置文件中没有足够的列:\033[1m\033[1;31m[%s]\033[1m\033[0m\a
请使用如下格式:
主机地址===端口号===使用了Key登陆此处可填写None===使用了Key登陆此处可填写None===su-root密码，如果没有配置使用su-root，此列填写None""" % b.strip()
					sys.exit()
				
				ServersUsername[a[0]]=a[2]
				ServersPassword[a[0]]=None
		T.close()
	except IndexError:
		print """您的主机文件中，没有足够的配置，正确的应该是:
主机列===端口列===账户名列===密码列===su-root密码列"""
		sys.exit()
	except Exception,e:
		print "读取配置错误 %s (%s) "%(e,HostsFile)
		sys.exit(1)
	try:
		Timeout=c.get("CheungSSH","Timeout")
		try:
			Timeout=socket.setdefaulttimeout(int(Timeout))
		except Exception,e:
			Timeout=socket.setdefaulttimeout(3)
	except Exception,e:
		Timeout=socket.setdefaulttimeout(3)

	#print "Servers:%d|RunMode:%s|Deployment:%s|UseKey:%s|CurUser:%s|Useroot:%s|sudo:%s  \n" % (len(ServersPort),RunMode,Deployment,UseKey,getpass.getuser(),Useroot,sudo)
	return ServersUsername,ServersPassword,HostsGroup,Servers
#def SSH_cmd(ip,username,password,port,cmd,UseLocalScript,OPTime):
def main(cmd,ie_key,selectserver="all"):
	Read_config()
	global Servers,ServersPassword,ServersPort,ServersUsername,FailIP,All_Servers_num,All_Servers_num_all,All_Servers_num_Succ
	if len(Servers)==0:
		print "当前没有配置可用主机，请在~/cheung/conf/hosts中配置主机信息！"
		sys.exit(1)
	All_Servers_num_Succ=0
	All_Servers_num=0
	FailIP=[]
	OPTime=time.strftime('%Y%m%d%H%M%S',time.localtime())
	if selectserver=="all":
		Servers_T=Servers
	else:
		Servers_T=selectHosts.selectServers(selectserver,Servers,HostsGroup)
	All_Servers_num_all=len(Servers_T)
	for a in Servers_T:
		#SSH_cmd(a,ServersUsername[a],ServersPassword[a],ServersPort[a],cmd,'N',OPTime)
		a=threading.Thread(target=SSH_cmd,args=(a,ServersUsername[a],ServersPassword[a],ServersPort[a],cmd,'N',OPTime,ie_key))
		a.start()
if __name__=='__main__':
	main("id","all","all")
	#os.system("""echo 'Done' >/tmp/status""")
