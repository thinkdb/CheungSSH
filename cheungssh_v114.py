#!/usr/bin/python
#coding:utf8
#Author=Cheung Kei-Chuen
#QQ 741345015
VERSION=114
import os,sys
BUILD_CMD=['exit','flush logs']
os.sys.path.insert(0,os.path.abspath('./'))
os.sys.path.insert(0,os.path.abspath('/cheung/bin/'))
try:
	import paramiko,threading,socket,ConfigParser,time,commands,threading,re,getpass,Format_Char_Show,shutil,random,getpass,LogCollect,readline
except Exception,e:
	print "\033[1m\033[1;31m-ERR %s\033[0m\a"	% (e)
	sys.exit(1)
reload(sys)
sys.setdefaultencoding('utf8')
LogFile='/cheung/logs/cheungssh.log'
SLogFile='/cheung/logs/cheungssh.source.log'
DeploymentFlag="/tmp/DeploymentFlag%s" % (str(random.randint(999999999,999999999999)))
try:
	paramiko.util.log_to_file('/cheung/logs/paramiko.log')
except Exception,e:
	pass
#os.system('stty erase ^H')
T_V=sys.version.split()[0]
if int(T_V.replace(".","")) <240:
	print "Python's version can not less than 2.4"
	print "Please : yum  update  -y  python"
	sys.exit(1)


def Write_Log(ip,stderr,stdout,Logcmd,LogFile,useroot,username,UseLocalScript,Deployment,DeploymentStatus,OPTime):
	os.system("chmod 777 /cheung/logs/* 2>/dev/null")
	if DeploymentStatus:
		DeploymentStatus_T='Y'
	else:
		DeploymentStatus_T='N'
	if UseKey=="Y":
		username=getpass.getuser()
	Deployment=Deployment.upper()
	
	try:
		T=open(LogFile,"a")
		T.write(ip+ '===' + "用户名:" +username  + '===' + "时间:"+OPTime   + '===' + "是否使用su-root:"+useroot + '===' + "是否使用脚本:" + UseLocalScript + '===' + "是否使用部署模式:"+Deployment + '===' +"部署完成状态"+ DeploymentStatus_T + '===' + "命令:"+Logcmd + '===' +"错误显示:"+ stderr + '===' +"正确显示:"+ stdout)
		T.close()
	except Exception,e:
		print "Warning: Can't write log. (%s)" % e
def WriteSourceLog(MSG):
	os.system("chmod 777 /cheung/logs/* 2>/dev/null")
	try:
		F=open(SLogFile,"a")
		F.write(MSG)
		F.close()
	except Exception,e:
		print "Can not write to source log (%s)" % (e)
def LocalScriptUpload(ip,port,username,password,s_file,d_file):
	try:		
		t = paramiko.Transport((ip,port))
                if UseKey=='Y':
                        KeyPath=os.path.expanduser('~/.ssh/id_rsa')
                        key=paramiko.RSAKey.from_private_key_file(KeyPath)
			t.connect(username = username,pkey=key)
		else:
			t.connect(username = username,password = password)
		sftp = paramiko.SFTPClient.from_transport(t)
		ret=sftp.put(s_file,d_file)
	except Exception,e:		
		print "LocalScript inited Failed",e
		return False	
	else:
		t.close()
def InitInstall():
	INITDIR="/cheung/logs /cheung/flag  /cheung/conf /cheung/bin /cheung/version"
	if not os.path.isdir("/cheung"):
		if commands.getstatusoutput("mkdir -p %s 2>/dev/null" % (INITDIR))[0]!=0:
			print "Must be as root Create config file!"
			sys.exit(1)
	else:
		os.system("mkdir  -p %s 2>/dev/null" % INITDIR)
	if not os.path.isfile('/cheung/conf/cheung.conf'):
		T=open('/cheung/conf/cheung.conf','w')
		T.write("""[CheungSSH]
#Author=Cheung Kei-Chuen
#QQ=741345015
Useroot=N
RunMode=M
#请在/cheung/cong/hosts中指定主机信息
#Timeout=3
#UseKey=N
#Deployment=N
#ListenFile=/var/log/messages
#ListenTime=60
#ListenChar=Server startup""")
		T.close()
	try:
		VerR=int(open("/cheung/version/version").read().strip())
	except Exception,e:
		VerR=0
	if VerR<104:
		os.system("""echo %s >/cheung/version/version 2>/dev/null"""%(VERSION))
		T=open('/cheung/conf/cheung.conf','w')
		T.write("""[CheungSSH]
#Author=Cheung Kei-Chuen
#QQ=741345015
Useroot=N
RunMode=M
#请在/cheung/cong/hosts中指定主机信息
#Timeout=3
#UseKey=N
#Deployment=N
#ListenFile=/var/log/messages
#ListenTime=60
#ListenChar=Server startup""")
		T.close()
		print "\033[1;33m您使用了新版本，相比之前的老版本在配置上会有所变化，请重新对\n/cheung/conf/cheung.conf\n/cheung/conf/hosts进行配置\a\033[0m"
	if not os.path.isfile('/cheung/conf/hosts'):
		T=open('/cheung/conf/hosts','w')
		T.write("""[Hosts-Name]
#主机地址===端口===登陆账户===登陆密码===su-root密码
#如果您担心安全问题，在密码列位置，您可以使用...===None===...表示不在配置文件中指定，而是在您执行命令的时候系统会询问您密码。比如以下配置:
#127.0.0.1===222===root===None===None
#locallhost===22===root===MyPassword===su-root的密码,如果没有使用Useroot，此列也可以填写None
#None的特殊指定只能针对密码特别指定，不能在账户名，或者是端口，主机这三列中使用
#注意:在每一个配置中，请不要有空格或者是制表符!
#在所有的配置列中，请用三个等于（===）分割开，并确保有5列！""")
		T.close()



def SSH_cmd(ip,username,password,port,cmd,UseLocalScript,OPTime):
	PROFILE=". /etc/profile 2&>/dev/null;. ~/.bash_profile 2&>/dev/null;. /etc/bashrc 2&>/dev/null;. ~/.bashrc 2&>/dev/null;"
	PATH="export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin;"
	global All_Servers_num,All_Servers_num_all,All_Servers_num_Succ,Done_Status,Global_start_time,PWD,FailIP
	start_time=time.time()
	ResultSum=''
	ResultSumLog=''
	DeploymentStatus=False
	DeploymentInfo=None
	PWD=re.sub("/{2,}","/",PWD)
	try:
		o=None
		err=None
		ssh=paramiko.SSHClient()
		if UseKey=='Y':
	
			KeyPath=os.path.expanduser('~/.ssh/id_rsa')
			###
			key=paramiko.RSAKey.from_private_key_file(KeyPath)
			ssh.load_system_host_keys()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,port,username,pkey=key)  
		else:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,port,username,password)
		if Deployment=='Y':
			stdin,stdout,stderr=ssh.exec_command(PROFILE+PWD+PATH+ListenLog+cmd)
		else:
			stdin,stdout,stderr=ssh.exec_command(PROFILE+PWD+PATH+cmd)
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
			ResultSum_count="\033[1m\033[1;32m+OK %s (%0.2f Sec, All %d Done %d \033[1m\033[1;31mCmd:Failed\033[1m\033[1;32m)\033[1m\033[0m" % (ip,float(time.time()-start_time),All_Servers_num_all,All_Servers_num)
			out='Null\n'
			if Deployment=='Y':
				DeploymentStatus=False
			Write_Log(ip,ResultSumLog.strip('\\n'),out,cmd,LogFile,'N',username,UseLocalScript,Deployment,DeploymentStatus,OPTime)
		else:
			error_out='NULL'
			ResultSum_count="\033[1m\033[1;32m+OK %s (%0.2f Sec, All %d Done %d  Cmd:Sucess)\033[1m\033[0m" % (ip,float(time.time()-start_time),All_Servers_num_all,All_Servers_num)
			All_Servers_num_Succ+=1
			if Deployment=='Y':
				print  "Wating %s deployment (for %d Sec)..." % (ip,ListenTime)
				T=LogCollect.LogCollect(ip,port,username,password,"""grep  -E "%s"  %s -q && echo  -n 'DoneSucc'""" % (ListenChar,DeploymentFlag),ListenTime,UseKey)
				if T:
					DeploymentStatus=True
				else:
					DeploymentInfo="Main commands excuted success, But deployment havn't check suncess info (%s) " %(ListenChar)
					DeploymentStatus=False
					

			Write_Log(ip,error_out,ResultSumLog.strip('\\n') + '\n',cmd,LogFile,'N',username,UseLocalScript,Deployment,DeploymentStatus,OPTime)

		Show_Result=ResultSum + '\n' +ResultSum_count
		TmpShow=Format_Char_Show.Show_Char(Show_Result+"Time:"+OPTime,0)  
		WriteSourceLog(TmpShow)
		print TmpShow
	except Exception,e:
		FailIP.append(ip)
		All_Servers_num += 1
		ResultSum_count="\n\033[1m\033[1;31m-ERR %s %s (%0.2f Sec All %d Done %d)\033[1m\033[0m\a"	% (ip,e,float(time.time() - start_time),All_Servers_num_all,All_Servers_num)
		Show_Result= ResultSum+ResultSum_count

                TmpShow=Format_Char_Show.Show_Char(Show_Result+"Time:"+OPTime,0)
                WriteSourceLog(TmpShow)
                print TmpShow
		#Format_Char_Show.Show_Char(Show_Result+"Time:"+OPTime,1)  
		Write_Log(ip,str(e),'NULL\n',cmd,LogFile,'N',username,UseLocalScript,Deployment,DeploymentStatus,OPTime)
	else:
		ssh.close()
	if Deployment=='Y' and not  DeploymentStatus:
		while True:
			TT=raw_input("%s Deployment not Success (%s) want contiue deployment next server (yes/no) ? " %(ip,DeploymentInfo))
			if TT=='yes':
				break
			elif TT=='no':
				sys.exit(1)
	if All_Servers_num == All_Servers_num_all: #这里防止计数器永远相加下去
		FailNum=All_Servers_num_all-All_Servers_num_Succ
		if FailNum>0:
			FailNumShow="\033[1m\033[1;31mFail:%d\033[1m\033[0m" % (FailNum)
		else:
			FailNumShow="Fail:%d" % (FailNum)
		print "+Done (Succ:%d,%s, %0.2fSec CheungSSH(V:%d) Cheung Kei-Chuen All Right Reserved)" % (All_Servers_num_Succ,FailNumShow,time.time()-Global_start_time,VERSION)
		All_Servers_num =0
		All_Servers_num_Succ=0
		Done_Status='end'

def Read_config(file="/cheung/conf/cheung.conf"):
	global Servers,Useroot,Timeout,RunMode,UseKey,Deployment,ListenTime,ListenFile,ListenChar,ServersPort,ServersPassword,ServersUsername,ServersRootPassword,NoPassword,NoRootPassword,HostsGroup
	ServersPort={};ServersPassword={};ServersUsername={};ServersRootPassword={};Servers=[];HostsGroup={}
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
		Deployment=c.get("CheungSSH","Deployment").upper()
		if Deployment=='Y':
			try:
				ListenFile=c.get("CheungSSH","ListenFile")
			except Exception,e:
				print "In deployment mode ,must be specify ListenFile"
				sys.exit(1)
			try:
				ListenTime=int(c.get("CheungSSH","ListenTime"))
			except Exception,e:
				print  "Warning : ListenTime default is 60"
				ListenTime=60
			try:
				ListenChar=c.get("CheungSSH","ListenChar")
			except Exception,e:
				print "In deployment mode ,must be specify ListenChar"
				sys.exit(1)
	except Exception,e:
		Deployment='N'
	if RunMode=='M' and Deployment=='Y':
		print "In Mutiple-threading mode,do not support deployment mode!"
		sys.exit(1)
			
		
	try:
		Useroot=c.get("CheungSSH","Useroot").upper()
		if Useroot=='Y' and Deployment=='Y':
			print "In Deployment no support su  - root "
			sys.exit(1)
	except Exception,e:
		Useroot="N"
	try:
		UseKey=c.get("CheungSSH","UseKey").upper()
	except:
		UseKey="N"
	try:
		HostsFile="/cheung/conf/hosts"
		T=open(HostsFile)
		NoPassword=False
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
					if not NoPassword:
						print "注意:\033[1;33m\n\t您在[%s]使用了None指定密码，程序将不会读取配置文件中的密码,而是需要您手动指定一个密码用于全部主机,如果这不是您需要的，请重新为每一个主机指定密码!\033[0m"%a[0]
						NoPassword=True
				else:
					ServersPassword[a[0]]=a[3]
						
			else:
				if len(a)<5:
					print """您的配置文件中没有足够的列:\033[1m\033[1;31m[%s]\033[1m\033[0m\a
请使用如下格式:
主机地址===端口号===使用了Key登陆此处可填写None===使用了Key登陆此处可填写None===su-root密码，如果没有配置使用su-root，此列填写None""" % b.strip()
					sys.exit()
				
				ServersUsername[a[0]]=getpass.getuser()
			NoRootPassword=False
			if Useroot.upper()=="Y":
				try:
					TK=re.search("^[Nn][Oo][Nn][Ee]$",a[4])
					if TK:
						if not NoRootPassword:
							NoRootPassword=True
					else:
						ServersRootPassword[a[0]]=a[-1]
				except Exception,e:
					print """您使用了su - root ，但未指定su - root的密码
%s===端口===账户名===密码===root的密码""" % (a[0])
					print e
					sys.exit()
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
			Timeout=3
			print "Warning: Timeout's Value Error, default=3 (Sec)"
	except Exception,e:
		Timeout=socket.setdefaulttimeout(10)

	print "Servers:%d|RunMode:%s|Deployment:%s|UseKey:%s|CurUser:%s|Useroot:%s  \n" % (len(ServersPort),RunMode,Deployment,UseKey,getpass.getuser(),Useroot)
def Upload_file(ip,port,username,password):
	start_time=time.time()
	global All_Servers_num,All_Servers_num_all,All_Servers_num_Succ,Global_start_time
	try:
		t = paramiko.Transport((ip,port))
		if UseKey=='Y':
                        KeyPath=os.path.expanduser('~/.ssh/id_rsa')
                        key=paramiko.RSAKey.from_private_key_file(KeyPath)
			try:
				t.connect(username = username,pkey=key)
			except EOFError:
				print "Try use RunMode=D"
			##########################################
		else:
			try:
				t.connect(username = username,password = password)
			except EOFError:
				print "Try use RunMode=D"
		sftp = paramiko.SFTPClient.from_transport(t)
		New_d_file=re.sub('//','/',d_file + '/')+ os.path.split(s_file)[1]
		Bak_File=New_d_file+'.bak.'+"%d" % (int(time.strftime("%Y%m%d%H%M%S",time.localtime(Global_start_time))))
		try:
			sftp.rename(New_d_file,Bak_File)
			SftpInfo="Warning: %s %s  already exists,backed up to %s \n" % (ip,New_d_file,Bak_File)
		except Exception,e:
			SftpInfo='\n'
		ret=sftp.put(s_file,New_d_file)
		All_Servers_num += 1
		All_Servers_num_Succ+=1
		print SftpInfo + "\033[1m\033[1;32m+OK %s (%0.2f Sec  All %d Done %d)\033[1m\033[0m" % (ip,time.time() - start_time,All_Servers_num_all,All_Servers_num)
	except Exception,e:
		All_Servers_num += 1
		print "\033[1m\033[1;31m-ERR %s %s(%0.2f Sec,All %d Done %d)\033[1m\033[0m" % (ip,e,float(time.time() -start_time),All_Servers_num_all,All_Servers_num)	
	else:
		t.close()

	if All_Servers_num_all == All_Servers_num:
		FailNum=All_Servers_num_all-All_Servers_num_Succ
		if FailNum>0:
			FailNumShow="\033[1m\033[1;31mFail:%d\033[1m\033[0m" % (FailNum)
		else:
			FailNumShow="Fail:%d" % (FailNum)
		
		print "+Done (Succ:%d,%s, %0.2fSec CheungSSH(V:%d) Cheung Kei-Chuen All Right Reserved)" % (All_Servers_num_Succ,FailNumShow,time.time()-Global_start_time,VERSION)
		All_Servers_num =0
		All_Servers_num_Succ=0


def Download_file_regex(ip,port,username,password):
	global All_Servers_num_all,All_Servers_num,All_Servers_num_Succ
	start_time=time.time()
	try:
		t = paramiko.Transport((ip,port))
                if UseKey=='Y':
                        KeyPath=os.path.expanduser('~/.ssh/id_rsa')
                        key=paramiko.RSAKey.from_private_key_file(KeyPath)
			t.connect(username = username,pkey=key)
		else:
			t.connect(username = username,password = password)
		sftp = paramiko.SFTPClient.from_transport(t)
		t_get=sftp.listdir(os.path.dirname(s_file))
		for getfilename in t_get:
			if re.search(os.path.basename(s_file),getfilename):
				download_fullpath=os.path.join(os.path.dirname(s_file),getfilename)
				try:
					ret=sftp.get(download_fullpath,"%s_%s" % (os.path.join(d_file,getfilename),ip))
					print  '\t\033[1m\033[1;32m+OK %s : %s' % (ip,download_fullpath)
				except Exception,e:
					print  '\t\033[1m\033[1;33m-Failed %s : %s %s' % (ip,download_fullpath,e)
		All_Servers_num +=1
		All_Servers_num_Succ+=1
		print "\033[1m\033[1;32m+OK %s (%0.2f Sec All %d Done %d)\033[1m\033[0m" % (ip,float(time.time()) - start_time,All_Servers_num_all,All_Servers_num)
	except Exception,e:
		All_Servers_num +=1
		print "\033[1m\033[1;31m-ERR %s %s (%0.2f Sec All %d Done %d)\033[1m\033[0m" % (ip,e,float(time.time() - start_time),All_Servers_num_all,All_Servers_num)
	else:
		t.close()
	if All_Servers_num_all == All_Servers_num:
		All_Servers_num = 0
		FailNum=All_Servers_num_all-All_Servers_num_Succ
		if FailNum>0:
			FailNumShow="\033[1m\033[1;31mFail:%d\033[1m\033[0m" % (FailNum)
		else:
			FailNumShow="Fail:%d" % (FailNum)
		print "+Done (Succ:%d,%s, %0.2fSec CheungSSH(V:%d) Cheung Kei-Chuen All Right Reserved)" % (All_Servers_num_Succ,FailNumShow,time.time()-Global_start_time,VERSION)
		

def Download_file(ip,port,username,password):
	global All_Servers_num_all,All_Servers_num,All_Servers_num_Succ
	start_time=time.time()
	try:
		t = paramiko.Transport((ip,port))
                if UseKey=='Y':
                        KeyPath=os.path.expanduser('~/.ssh/id_rsa')
                        key=paramiko.RSAKey.from_private_key_file(KeyPath)
			t.connect(username = username,pkey=key)
               	else:
			t.connect(username = username,password = password)
		sftp = paramiko.SFTPClient.from_transport(t)
		New_d_file=re.sub('//','/',d_file + '/')
		ret=sftp.get(s_file,"%s%s_%s" % (New_d_file,os.path.basename(s_file),ip))
		All_Servers_num +=1
		All_Servers_num_Succ+=1
		print "\033[1m\033[1;32m+OK %s (%0.2f Sec All %d Done %d)\033[1m\033[0m" % (ip,float(time.time()) - start_time,All_Servers_num_all,All_Servers_num)
	except Exception,e:
		All_Servers_num +=1
		print "\033[1m\033[1;31m-ERR %s %s (%0.2f Sec All %d Done %d)\033[1m\033[0m" % (ip,e,float(time.time() - start_time),All_Servers_num_all,All_Servers_num)
	else:
		t.close()
	if All_Servers_num_all == All_Servers_num:
		All_Servers_num = 0
		FailNum=All_Servers_num_all-All_Servers_num_Succ
		if FailNum>0:
			FailNumShow="\033[1m\033[1;31mFail:%d\033[1m\033[0m" % (FailNum)
		else:
			FailNumShow="Fail:%d" % (FailNum)	
		print "+Done (Succ:%d,%s, %0.2fSec CheungSSH(V:%d) Cheung Kei-Chuen All Right Reserved)" % (All_Servers_num_Succ,FailNumShow,time.time()-Global_start_time,VERSION)





	
def Main_p():
	global s_file,d_file,All_Servers_num_Succ,LocalScript,Global_start_time,NoPassword,NoRootPassword
	global All_Servers_num_all,All_Servers_num
	#All_Servers_num_all=len(Servers.split(','))
	All_Servers_num    =0
	All_Servers_num_Succ=0
	if not Servers:
		print "当前没有配置服务器地址,请在/cheung/conf/hosts文件中配置!"
		sys.exit()
	try:
		from optparse import OptionParser
		p=OptionParser()
		p.add_option("-t","--excute-type",help="""Description: select excute type
			Parameter: [cmd|download|upload]
				cmd     : Excute Shell Command
				download: Download file
				upload  : Upload file
			
			Example: %s -t cmd""" % sys.argv[0])
		p.add_option("-s","--source-file",help="""Description:	Specific Source file  path
			Example:
				%s  -t upload   -s /local/file  -d /remote/dir
				%s  -t download -s /remote/file -d /local/dir""" %(sys.argv[0],sys.argv[0]))
		p.add_option("-d","--destination-file",help="""
			Description: Specific a destination directory Path""")
		p.add_option("-r","--regex",action='store_false',default=True,help="""
			Description: Use regex match filename
			Example: 
			%s  -t download -s '^/remote/tomcat/logs/localhost_2015-0[1-3].*log$' -d  /local/dir/

			Notice: This parameter applies only to download""" % sys.argv[0])
		(option,args)=p.parse_args()

		if NoPassword and UseKey=="N":
			SetPassword=getpass.getpass("请在此处为所有主机指定密码(请确保该密码适用用于所有的服务器，否则请在配置文件/cheung/conf/hosts文件中逐个指定)\n\033[1;33mHosts Password:\033[0m  ")
			if SetPassword:
				print "已为所有主机指定密码"
			else:
				print "您尚未指定密码，程序退出"
				sys.exit()
			for a in Servers:
				ServersPassword[a]=SetPassword
			NoPassword=False
		if Useroot=="Y":
			if NoRootPassword:
				SetRootPassword=getpass.getpass("请指定su-root的密码: ")
				if SetRootPassword:
					print  "已指定su - root密码"
					NoRootPassword=False
				else:
					print "您尚未指定su - root的密码,程序退出"
					sys.exit()
		if option.excute_type == "cmd":
			Excute_cmd()
		elif option.excute_type == "upload":
			All_Servers_num_all=len(Servers)
			if option.source_file and option.destination_file:
				s_file=option.source_file
				d_file=option.destination_file
			else:
				print "Upload File"
				s_file=raw_input("Local Source Path>>>")
				d_file=raw_input("Remote Destination Full-Path>>>")
			Global_start_time=time.time()
			for s in Servers:
				if RunMode.upper()=='M':
					if UseKey=="Y":
						a=threading.Thread(target=Upload_file,args=(s,ServersPort[s],ServersUsername[s],None))
					else:
						a=threading.Thread(target=Upload_file,args=(s,ServersPort[s],ServersUsername[s],ServersPassword[s]))
					a.start()
				else:
					if UseKey=="Y":
						Upload_file(s,ServersPort[s],ServersUsername[s],None)
					else:
						Upload_file(s,ServersPort[s],ServersUsername[s],ServersPassword[s])
		elif option.excute_type == "download":
			All_Servers_num_all=len(Servers)
			if option.source_file and option.destination_file:
				s_file=option.source_file
				d_file=option.destination_file
			else:
				print "Download File"
				s_file=raw_input("Remote Source Full-Path>>>")
				d_file=raw_input("Local Destination Path>>>")
			if not os.path.isdir(d_file):
				print 'Recv location must be a directory'
				sys.exit(1)
			Global_start_time=time.time()
			for s in Servers:
				if option.regex:
					if UseKey=="Y":
						a=threading.Thread(target=Download_file,args=(s,ServersPort[s],ServersUsername[s],None))
					else:
						a=threading.Thread(target=Download_file,args=(s,ServersPort[s],ServersUsername[s],ServersPassword[s]))
				else:
					if UseKey=="Y":
						a=threading.Thread(target=Download_file_regex,args=(s,ServersPort[s],ServersUsername[s],None))
					else:
						a=threading.Thread(target=Download_file_regex,args=(s,ServersPort[s],ServersUsername[s],ServersPassword[s]))
						
				a.start()
		elif not option.excute_type:
			Excute_cmd()
			sys.exit(0)
		else:
			print "Parameter does not currently support\t(%s)\a" % (option.excute_type)
			Excute_cmd()
	except KeyboardInterrupt:
		print "exit"
	except EOFError:
		print "exit"

def Excute_cmd_root(s,Port,Username,Password,Passwordroot,cmd,UseLocalScript,OPTime):
	global All_Servers_num_all,All_Servers_num,All_Servers_num_Succ,Done_Status,bufflog,FailIP
	Done_Status='start'
	bufflog=''
	start_time=time.time()
	ResultSum=''
	Result_status=False
	try:
		t=paramiko.SSHClient()
                if UseKey=='Y':
			KeyPath=os.path.expanduser('~/.ssh/id_rsa')
                        key=paramiko.RSAKey.from_private_key_file(KeyPath)
                        t.load_system_host_keys()
			t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        t.connect(s,Port,Username,pkey=key) 
                else:
			t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			t.connect(s,Port,Username,Password)
		ssh=t.invoke_shell()
		ssh.send("LANG=zh_CN.UTF-8\n")
		ssh.send("export LANG\n")
		ssh.send("su - root\n")
		buff=''
		while not re.search("Password:",buff) and not re.search("：", buff):
			resp=ssh.recv(9999)
			buff += resp
		ssh.send("%s\n" % (Passwordroot))
		buff1=''
		while True:
			resp=ssh.recv(500)
			buff1 += resp
			if  re.search('su:',buff1):
				#print "\033[1;31m-ERR su Failed  %s\033[0m" % (s)
				break
			else:
				if re.search('# *$',buff1):
					Result_status=True
                			All_Servers_num_Succ+=1
					break
		if Result_status:
			ssh.send(PWD)
			ssh.send("%s\n" % (cmd))
			buff=""
			bufflog=''
			while not buff.endswith("# "):
				resp=ssh.recv(9999)
				buff  += resp
				bufflog  += resp.strip('\r\n') + '\\n'
			t.close()
			All_Servers_num += 1
			ResultSum=buff + "\n\033[1m\033[1;32m+OK %s (%0.2f Sec All %d Done %d)\033[1m\033[0m\n" % (s,float(time.time() - start_time),All_Servers_num_all,All_Servers_num)
			
			bufflog_new=''
			for t in bufflog.split():
				if t==cmd:
					continue
				bufflog_new+=t
			bufflog=bufflog_new
		else:
			All_Servers_num += 1
			FailIP.append(s)
			ResultSum=buff + "\n\033[1m\033[1;31m-ERR Su Failed %s (%0.2f Sec All %d Done %d)\033[1m\033[0m\n" % (s,float(time.time() - start_time),All_Servers_num_all,All_Servers_num)
			
	except Exception,e:
		All_Servers_num += 1
		Result_status=False
		FailIP.append(s)
		ResultSum="\n\033[1m\033[1;31m-ERR %s %s (%0.2f Sec All %d Done %d)\033[1m\033[0m\a"   % (e,s,float(time.time() - start_time),All_Servers_num_all,All_Servers_num)
		bufflog=str(e)
	if Result_status:
		Write_Log(s,'NULL',bufflog.strip('\\n') + '\n',cmd,LogFile,'Y',Username,UseLocalScript,'N','N',OPTime)
		#TmpShow=Format_Char_Show.Show_Char(Show_Result+"Time:"+OPTime,0)
		TmpShow=Format_Char_Show.Show_Char(ResultSum+"Time:"+OPTime,0)
		WriteSourceLog(TmpShow)
		print TmpShow
		#Format_Char_Show.Show_Char(ResultSum+"Time:"+OPTime,0)
	else:
		Write_Log(s,bufflog.strip('\\n'),'NULL\n',cmd,LogFile,'Y',Username,UseLocalScript,'N','N',OPTime)
		#TmpShow=Format_Char_Show.Show_Char(Show_Result+"Time:"+OPTime,0)
		TmpShow=Format_Char_Show.Show_Char(ResultSum+"Time:"+OPTime,0)
		WriteSourceLog(TmpShow)
		print TmpShow
		#Format_Char_Show.Show_Char(ResultSum+"Time:"+OPTime,1)
	if All_Servers_num_all == All_Servers_num:
		FailNum=All_Servers_num_all-All_Servers_num_Succ
		if FailNum>0:
			FailNumShow="\033[1m\033[1;31mFail:%d\033[1m\033[0m" % (FailNum)
		else:
			FailNumShow="Fail:%d" % (FailNum)
		print "+Done (Succ:%d,%s, %0.2fSec CheungSSH(V:%d) Cheung Kei-Chuen All Right Reserved)" % (All_Servers_num_Succ,FailNumShow,time.time()-Global_start_time,VERSION)
                All_Servers_num =0
                All_Servers_num_Succ=0
		Done_Status='end'

def Excute_cmd():
	global All_Servers_num_all,All_Servers_num,All_Servers_num_Succ,Done_Status,Logcmd,ListenLog,Global_start_time,PWD,FailIP,ScriptFilePath
	Done_Status='end'
	All_Servers_num    =0
	All_Servers_num_Succ=0
	UseLocalScript='N' #
	PWD='~'
	IS_PWD=False
	UseSystem=False
	Servers_T=Servers
	FailIP=[];LastCMD=[]
	if Useroot=="Y":
		CmdPrompt="CheungSSH root"
	else:
		CmdPrompt="CheungSSH"
	while True:
		All_Servers_num_all=len(Servers_T)
		OPTime=time.strftime('%Y%m%d%H%M%S',time.localtime())
			
		if Done_Status=='end':
			try:
				if IS_PWD:
					ShowPWD=re.sub(";$","",PWD.split()[1])
					ShowPWD=re.sub("/{2,}","/",ShowPWD)
					ShowPWD=re.sub("cd *","",ShowPWD)
				else:
					ShowPWD=re.sub(";$|cd *","",PWD)
			except Exception,e:
				ShowPWD=PWD
				pass
			cmd=raw_input("%s %s>>>> " % (CmdPrompt,ShowPWD  ))
		else:
			time.sleep(0.05)
			continue
		cmd=re.sub('^ *ll','ls -l',cmd)
		try:
			if not IS_PWD:
				if re.search("^ *cd.*",cmd):
					try:
						cmd.split()[1]
					except IndexError:
						PWD="cd ~;"
						continue
					PWD=re.search("^ *cd.*",cmd).group() +";"
					IS_PWD=True
					if not os.path.isfile("/cheung/flag/.NoAsk"):
						AskNotice=raw_input("\033[1;33m注意: 请您确保切换的路径[%s]在远程服务器上是存在的，否则切换路径没有任何意义,您清楚了吗？\033[0m(yes/no) " % (re.sub("^ *cd *|;","",PWD)))
						if re.search("[Yy]([Ee][Ss])?",AskNotice):
							AskCancel=raw_input("是否取消以上提示？(yes/no) ")
							if re.search("[Yy]([Ee][Ss])?",AskCancel):
								try:
									os.mknod("/cheung/flag/.NoAsk")
									os.system("chmod 777 /cheung/flag/.NoAsk")
									print "已取消提醒"
								except Exception,e:
									print "抱歉，不能取消提示(%s)" %e
						else:
							print "如果您对以上提示不清楚,那么那您可以在远程服务器上手动%s 那一定会报错的，所以请确保[%s]有效!" % (re.sub(";","",PWD),re.sub("^ *cd *|;","",PWD))
							sys.exit()



					continue
				else:
					if PWD=="~":
						PWD="cd %s;" % PWD
			else:
				try:
					if re.search("^ *cd.*",cmd):
						try:
							cmd.split()[1]
						except IndexError:
							PWD="cd ~;"
							continue
						if re.search("^[a-zA-Z].*",cmd.split()[1]):
							PWD=PWD.strip(";")+"/" +re.search("^[a-zA-Z].*",cmd.split()[1]).group()+";"
						else:
							PWD=cmd +";"
						
						IS_PWD=True
						continue
				except Exception,e:
					pass
		except Exception,e:
			if IS_PWD:
				PWD=PWD
			else:
				PWD="cd %s;" % PWD
		if re.search("^ *[Rr][Uu][Nn]",cmd):
			try:
				ScriptFilePath=cmd.split()[1]
				if not os.path.isfile(ScriptFilePath):
					print "您指的定程序[%s]不存在！" % ScriptFilePath
					continue
				else:
					ScriptFlag=str(random.randint(999999999,999999999999))
					d_file='/tmp/' + os.path.basename(ScriptFilePath) + ScriptFlag
					for s in Servers_T:
						d_file='/tmp/' + os.path.basename(ScriptFilePath) + ScriptFlag
						if UseKey=="Y":
							LocalScriptUpload(s,ServersPort[s],ServersUsername[s],None,ScriptFilePath,d_file)
						else:
							LocalScriptUpload(s,ServersPort[s],ServersUsername[s],ServersPassword[s],ScriptFilePath,d_file)
					Newcmd="""chmod a+x %s;%s;rm -f %s""" %(d_file,d_file,d_file)
					UseLocalScript="Y"
					Logcmd=ScriptFilePath
			except IndexError:
				print "您尚未指定本服务器上的脚本路径 用法: run /path/scriptfile"
				continue
		else:
			UseLocalScript="N"
			Newcmd=cmd
			Logcmd=cmd

		if re.search("^ *[Ee][Xx][Ii][Tt] *",cmd):
			sys.exit(0)
		if re.search("^ *[Cc][Ll][Ee][Aa][Rr] *",cmd):
			os.system("clear")
			continue
		if re.search('^ *[Ff][Ll][Uu][Ss][Hh] *[Ll][Oo][Gg][Ss] *$',cmd):
			try:
				Log_Flag=time.strftime('%Y%m%d%H%M%S',time.localtime())
				shutil.move('/cheung/logs/cheungssh.log','/cheung/logs/cheungssh%s.log' % Log_Flag)
				print "+OK"
				continue
			except Exception,e:
				print "Waring : %s Failed (%s)" % (cmd,e)
				continue
		if re.search("^ *$",cmd):
			continue
		if re.search("^ *vi",cmd):
			print "抱歉，当前不支持交互式"
			continue
		cmd=re.sub("^ *top","top  -b -d 1 -n 1",cmd)
		cmd=re.sub("^ *ping","ping  -c 4",cmd)
		if re.search("^ *[Uu][Ss][Ee] +[Ss]",cmd):
			if UseSystem==True:
				print "当前已经是Use sys模式"
			else:
				UseSystem=True
				CmdPrompt="%s conf" % (CmdPrompt)
			continue
		if UseSystem:
			if re.search("^ *[Ss][Hh][Oo][Ww] *",cmd):
				print "所有主机地址	: %s" % Servers
				print "当前可接受命令的主机	: %s" %Servers_T
				print """主机组:"""
				for B in HostsGroup:
					print "\t%s组主机: %s" % (B,HostsGroup[B])
				if LastCMD:
					print "执行命令%s失败的的主机	: %s" % (LastCMD,FailIP)
				continue
			elif re.search("^ *[Ss][Ee][Ll][Ee][Cc][Tt] *",cmd):
				try:
					SelectFailIP=cmd.split()[1]
					T=re.search("[Ff] *|[Aa][Ii][Ll] *",SelectFailIP)
					if T:
						if not FailIP:
							print "当前没有执行命令失败的主机,无法选定"
						else:
							Servers_T=FailIP
						continue
				except IndexError:
					print  "您尚未选定主机 select 主机地址"
					continue
				SelectServer=re.sub("^ *[Ss][Ee][Ll][Ee][Cc][Tt] *| *","",cmd).lower()
				if re.search("^ *[Aa][Ll]{2} *",SelectServer):
					Servers_T=Servers
					print "已选定所有主机: %s" % (Servers_T)
					continue
				IsSelectHostsGroup=False
				Host_I_Flag=True
				Any_In_HostsGroup=False
				for c in SelectServer.split(","):
					if c in HostsGroup.keys():
						if Host_I_Flag:
							Servers_T=HostsGroup[c]
							Host_I_Flag=False
						else:
							Servers_T=HostsGroup[c]+Servers_T
						IsSelectHostsGroup=True
						Any_In_HostsGroup=True
					elif Any_In_HostsGroup:
						print "您选定的当前主机组: [%s] 不在hosts配置文件中，请重新选定" % c
						continue
				if IsSelectHostsGroup:
					print "您已经选定主机组 : %s" %Servers_T
					IsSelectHostsGroup=False
					continue
				SelectFail=False
				for a in SelectServer.split(","):
					if not a in Servers:
						print "您选定的服务器%s不在配置文件中，所以选定失败,请重新选定" % a
						SelectFail=True
						break
						
				if SelectFail:
					SelectFail=False
					continue
				Servers_T=[]
				for a in SelectServer.split(','):
					Servers_T.append(a)
				print "您选定的远程服务器是：",Servers_T
				continue
			elif re.search("^ *[Nn][Oo] +[Uu] *",cmd):
				UseSystem=False
				CmdPrompt="%s" % (re.sub(" conf","",CmdPrompt))
				print "已退出配置模式"
				continue
			elif re.search("^ *[Nn][Oo] +[Ss][Ee][Ll][Ee][Cc][Tt] *$",cmd):
				Servers_T=Servers
				print "取消选定主机"
				continue
			elif re.search("^ *[Nn][Oo] +[Aa]|[Ll]{2} *$",cmd):
				Servers_T=Servers
				UseSystem=False
				print "已取消所有设置"
				continue
			elif re.search("^ *\? *$",cmd) or re.search("^ *[Hh]([Ee][Ll][Pp])? *$",cmd):
				print """内部命令：
	use     system      进入CheungSSH内部系统命令
	no      use         退出配置模式
	no      select      取消选定的主机,回复配置文件中指定的主机
	no      all         取消在配置模式中的所有设置
	select  hostname    选定一个或者多个主机，多个主机用逗号 "," 分开前提是这些主机必须在配置文件中已经配置好了
	select	fail        选定失败的主机
	select  all	    选定所有主机
	select  HostsGroupName 选定主机组
	show                显示主机分布情况"""
				continue
			else:
				print "抱歉，CheungSSH暂时不支持您输入的内部命令,如果要执行Linux命令，请使用no use退出"
				continue
		else:
			IsBack=False
			if re.search("^ *[Ss][Hh][Oo][Ww] *",cmd):
				IsBack=True
			elif re.search("^ *[Ss][Ee][Ll][Ee][Cc][Tt] *",cmd):
				IsBack=True
			elif re.search("^ *[Nn][Oo] +[Aa]|[Ll]{2} *$",cmd):
				print re.search("^ *[Nn][Oo] +[Aa]|[Ll]{2} *$",cmd).group()
				IsBack=True
			elif re.search("^ *[Nn][Oo] +[Uu][Ss][Ee] *$",cmd):
				IsBack=True
			elif re.search("^ *[Nn][Oo] +[Ss][Ee][Ll][Ee][Cc][Tt] *$",cmd):
				IsBack=True
			if IsBack:
				print "该命令是内部命令，请使用use sys进入配置模式执行"
				IsBack=False
				continue
		if len(Servers_T)==0:
			print "\033[1;33m当前没有设定服务器地址,或者选定的主机组中的服务器列表为空\033[0m"
			continue

		Global_start_time=time.time()
		FailIP=[]
		LastCMD=cmd
		ScriptFlag=str(random.randint(999999999,999999999999))
		Done_Status='start'
		for s in Servers_T:
			if RunMode.upper()=='M':
				if Useroot=='Y':
					if UseKey=="Y":
						a=threading.Thread(target=Excute_cmd_root,args=(s,ServersPort[s],ServersUsername[s],None,ServersRootPassword[s],Newcmd,UseLocalScript,OPTime))
					else:
						a=threading.Thread(target=Excute_cmd_root,args=(s,ServersPort[s],ServersUsername[s],ServersPassword[s],ServersRootPassword[s],Newcmd,UseLocalScript,OPTime))
					a.start()
				else:
					if UseKey=="Y":
						a=threading.Thread(target=SSH_cmd,args=(s,ServersUsername[s],None,ServersPort[s],Newcmd,UseLocalScript,OPTime))
					else:
						a=threading.Thread(target=SSH_cmd,args=(s,ServersUsername[s],ServersPassword[s],ServersPort[s],Newcmd,UseLocalScript,OPTime))

					a.start()
					
			else:
				if Useroot=='Y':
					if UseKey=="Y":
						Excute_cmd_root(s,ServersPort[s],ServersUsername[s],None,ServersRootPassword[s],Newcmd,UseLocalScript,OPTime)
					else:
						Excute_cmd_root(s,ServersPort[s],ServersUsername[s],ServersPassword[s],ServersRootPassword[s],Newcmd,UseLocalScript,OPTime)
				else:
					if Deployment=='Y':
						ListenLog="""if [ ! -r %s ] ; then echo -e '\033[1m\033[1;31m-ERR ListenFile %s  not exists,so do not excute commands !\033[1m\033[0m\a ' 1>&2 ;exit;else nohup tail -n 0 -f  %s  2&>%s &   fi;""" % (ListenFile,ListenFile,ListenFile,DeploymentFlag)
					SSH_cmd(s,ServersUsername[s],ServersPassword[s],ServersPort[s],Newcmd,UseLocalScript,OPTime)
							
			############################################################################################
if  __name__=='__main__':
	InitInstall()
	Read_config()
	Main_p()
