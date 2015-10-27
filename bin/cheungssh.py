#!/usr/bin/python
#coding:utf8
#Author=Cheung Kei-Chuen
#QQ=2418731289
VERSION=130
import os,sys
import commands
HOME=commands.getoutput('''echo "$HOME"''')
os.sys.path.insert(0,os.path.abspath('./'))
os.sys.path.insert(0,os.path.abspath('%s/cheung/bin/'%HOME))
try:
	import paramiko,threading,socket,ConfigParser,time,commands,threading,re,getpass,Format_Char_Show,shutil,random,getpass,LogCollect,readline,filemd5,command_tab,GetFile,UpdateFile
except Exception,e:
	print "\033[1m\033[1;31m-ERR %s\033[0m\a"	% (e)
	sys.exit(1)
reload(sys)
HOME=commands.getoutput('''echo "$HOME"''')
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
def SSH_cmd(conf):
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
			ResultSum_count="\033[1m\033[1;32m+OK [%s@%s] (%0.2f Sec, %d/%d \033[1m\033[1;31mCmd:Failed\033[1m\033[1;32m)\033[1m\033[0m" % (username,ip,float(time.time()-start_time),All_Servers_num,All_Servers_num_all)
			out='Null\n'
			if Deployment=='Y':
				DeploymentStatus=False
			Write_Log(ip,ResultSumLog.strip('\\n'),out,cmd,LogFile,'N',username,UseLocalScript,Deployment,DeploymentStatus,OPTime)
		else:
			error_out='NULL'
			ResultSum_count="\033[1m\033[1;32m+OK [%s@%s] (%0.2f Sec, %d/%d  Cmd:Sucess)\033[1m\033[0m" % (username,ip,float(time.time()-start_time),All_Servers_num,All_Servers_num_all)
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
		ResultSum_count="\n\033[1m\033[1;31m-ERR [%s@%s] %s (%0.2f Sec %d/%d)\033[1m\033[0m\a"	% (username,ip,e,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
		Show_Result= ResultSum+ResultSum_count

                TmpShow=Format_Char_Show.Show_Char(Show_Result+"Time:"+OPTime,1)
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
		sudo=c.get("CheungSSH","sudo")
	except:
		sudo=False
	if Useroot=='Y'  and sudo:
		print "您已经su-root了，不能再配置sudo，可以sudo=N后，使用su-root"
		sys.exit(1)
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
			if Useroot.upper()=="Y":
				try:
					TK=re.search("^[Nn][Oo][Nn][Ee]$",a[4])
					if TK:
						NoRootPassword=True
						ServersRootPassword[a[0]]=None
					else:
						ServersRootPassword[a[0]]=a[4]
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
			Timeout=socket.setdefaulttimeout(3)
	except Exception,e:
		Timeout=socket.setdefaulttimeout(3)

	print "Servers:%d|RunMode:%s|Deployment:%s|UseKey:%s|CurUser:%s|Useroot:%s|sudo:%s  \n" % (len(ServersPort),RunMode,Deployment,UseKey,getpass.getuser(),Useroot,sudo)
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
		print SftpInfo + "\033[1m\033[1;32m+OK [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m" % (username,ip,time.time() - start_time,All_Servers_num,All_Servers_num_all)
	except Exception,e:
		All_Servers_num += 1
		print "\033[1m\033[1;31m-ERR [%s@%s] %s(%0.2f Sec,All %d Done %d)\033[1m\033[0m" % (username,ip,e,float(time.time() -start_time),All_Servers_num,All_Servers_num_all)	
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
					print  '\t\033[1m\033[1;32m+OK [%s@%s] : %s' % (username,ip,download_fullpath)
				except Exception,e:
					print  '\t\033[1m\033[1;33m-Failed %s : %s %s' % (ip,download_fullpath,e)
		All_Servers_num +=1
		All_Servers_num_Succ+=1
		print "\033[1m\033[1;32m+OK [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m" % (username,ip,float(time.time()) - start_time,All_Servers_num,All_Servers_num_all)
	except Exception,e:
		All_Servers_num +=1
		print "\033[1m\033[1;31m-ERR [%s@%s] %s (%0.2f Sec  %d/%d)\033[1m\033[0m" % (username,ip,e,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
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
		print "\033[1m\033[1;32m+OK [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m" % (username,ip,float(time.time()) - start_time,All_Servers_num,All_Servers_num_all)
	except Exception,e:
		All_Servers_num +=1
		print "\033[1m\033[1;31m-ERR [%s@%s] %s (%0.2f Sec %d/%d)\033[1m\033[0m" % (username,ip,e,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
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
	global s_file,d_file,All_Servers_num_Succ,LocalScript,Global_start_time,NoPassword,NoRootPassword,ServersRootPassword
	global All_Servers_num_all,All_Servers_num,ServersPassword
	#All_Servers_num_all=len(Servers.split(','))
	All_Servers_num    =0
	All_Servers_num_Succ=0
	if not Servers:
		print "当前没有配置服务器地址,请在%s/cheung/conf/hosts文件中配置!" %HOME
		sys.exit()
	os.system("rm -f %s/cheung/data/hosts/* 2&>/dev/null"%HOME)
	for a in Servers:
		try:
			os.mknod("%s/cheung/data/hosts/%s"%(HOME,a))
		except Exception,e:
			pass
	os.system("touch %s/cheung/data/hosts/fail %s/cheung/data/hosts/all 2&>/dev/null"%(HOME,HOME))
	for a in HostsGroup:
		try:
			os.mknod("%s/cheung/data/hosts/%s"%(HOME,a))
		except Exception,e:
			pass
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
			SetPassword=getpass.getpass("请在此处为在密码列填写了[None]的主机指定密码,如果没有填写None的主机，密码依然读取配置文件中的信息(请确保您输入的密码适用于所有密码列填写了None的主机，否则请在配置文件%s/cheung/conf/hosts文件中逐个指定)\n\033[1;33mHosts Password:\033[0m  "%HOME)
			if SetPassword:
				print "已为所有主机指定密码"
			else:
				print "您尚未指定密码，程序退出"
				sys.exit()
			for a in Servers:
				if ServersPassword[a] is None:
					ServersPassword[a]=SetPassword
			NoPassword=False
		if Useroot=="Y":
			if NoRootPassword:
				SetRootPassword=getpass.getpass("请指定su-root的密码 (仅适用于您填写了None列的主机,没有填写None列的主机依然读取配置中的密码): ")
				if SetRootPassword:
					print  "已指定su - root密码"
					for a in Servers:
						if  ServersRootPassword[a] is None:
							ServersRootPassword[a]=SetRootPassword
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
						if  float(sys.version[:3])<2.6:
							Upload_file(s,ServersPort[s],ServersUsername[s],ServersPassword[s])
						else:
							a=threading.Thread(target=Upload_file,args=(s,ServersPort[s],ServersUsername[s],ServersPassword[s]))
							a.start()
							
					else:
						if  float(sys.version[:3])<2.6:
							Upload_file(s,ServersPort[s],ServersUsername[s],ServersPassword[s])
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
			if not os.path.isfile("%s/cheung/flag/.NoTabAsk"%HOME):
				TabAsk=raw_input("在新版本中，已经支持TAB补全功能，但是补全的依据是根据您当前所在的这个服务器上的路径为标准的，而并不是远程服务器上的路径，所以您需要确保使用TAB补全后，路径是正确的\n是否取消提示 (yes/no) ")
				if re.search("^ *[Yy]([Ee][Ss])? *$",TabAsk):
					try:
						os.mknod("%s/cheung/flag/.NoTabAsk"%HOME)
						print "已取消提醒"
					except Exception,e:
						print "取消提醒失败(%s)" % e
					
			Excute_cmd()
			sys.exit(0)
		else:
			print "Parameter does not currently support\t(%s)\a" % (option.excute_type)
			Excute_cmd()
	except KeyboardInterrupt:
		print "exit"
	except EOFError:
		print "exit"

def Excute_sudo(s,Port,username,Password,cmd,UseLocalScript,OPTime):
	global All_Servers_num_all,All_Servers_num,All_Servers_num_Succ,Done_Status,bufflog,FailIP,PWD,sudo
	PWD=re.sub("/{2,}","/",PWD)
	Done_Status='start'
	bufflog=''
	start_time=time.time()
	ResultSum=''
	Result_status=False
	sudoinfo=re.sub("^ *| *$","",sudo).split()
	if username=='root':
		print "不能用root登陆后再sudo登陆"
		sys.exit()
	elif sudoinfo[-1]=='-' or sudoinfo[-1]=='root' or  sudoinfo[-1]=='su':
		prompt='# '
	else:
		prompt='$ '
	try:
		t=paramiko.SSHClient()
                if UseKey=='Y':
			KeyPath=os.path.expanduser('~/.ssh/id_rsa')
                        key=paramiko.RSAKey.from_private_key_file(KeyPath)
                        t.load_system_host_keys()
			t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        t.connect(s,Port,username,pkey=key) 
                else:
			t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			t.connect(s,Port,username,Password)
		ssh=t.invoke_shell()
		ssh.send("LANG=zh_CN.UTF-8\n")
		ssh.send("export LANG\n")
		ssh.send("%s\n"%sudo)
		buff=''
		resp=''
		info=''
		EnterPassword=False
		while True:
			if re.search("\[sudo\] +password for.*:",resp):
				ssh.send("%s\n"%Password)
				while True:
					resp=ssh.recv(100)
					if re.search("Sorry, try again",resp):
						info='密码错误'
						break
					elif re.search('%s +.*sudoers'%username,resp):
						info="没有sudo权限"
						break
					elif resp.endswith(prompt):
						EnterPassword=True
						Result_status=True
						break
			if EnterPassword:break
			if buff.endswith(prompt):
				Result_status=True
				break
			if re.search('%s +.*sudoers'%username,resp):
				info="没有sudo权限"
				break
			resp=ssh.recv(9999)
			buff += resp
		if Result_status:
			ssh.send("%s\n" % (PWD+cmd))
			buff=""
			bufflog=''
			while not buff.endswith(prompt):
				resp=ssh.recv(9999)
				buff  += resp
				bufflog  += resp.strip('\r\n') + '\\n'
			t.close()
			All_Servers_num += 1
			buff='\n'.join(buff.split('\r\n')[1:][:-1])
			ResultSum=buff + "\n\033[1m\033[1;32m+OK [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m\n" % (username,s,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
			
			bufflog_new=''
			for t in bufflog.split():
				if t==cmd:
					continue
				bufflog_new+=t
			bufflog=bufflog_new
			All_Servers_num_Succ+=1
		else:
			All_Servers_num += 1
			FailIP.append(s)
			#buff=''.join(buff.split('\r\n')[:-1])+'\n'
			buff=''
			
			ResultSum=buff + "\n\033[1m\033[1;31m-ERR sudo Failed (%s) [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m\n" % (info,username,s,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
			
	except Exception,e:
		All_Servers_num += 1
		Result_status=False
		FailIP.append(s)
		ResultSum="\n\033[1m\033[1;31m-ERR %s [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m\a"   % (e,username,s,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
		bufflog=str(e)
	if Result_status:
		Write_Log(s,'NULL',bufflog.strip('\\n') + '\n',cmd,LogFile,'Y',username,UseLocalScript,'N','N',OPTime)
		TmpShow=Format_Char_Show.Show_Char(ResultSum+"Time:"+OPTime,0)
		WriteSourceLog(TmpShow)
	else:
		Write_Log(s,bufflog.strip('\\n'),'NULL\n',cmd,LogFile,'Y',username,UseLocalScript,'N','N',OPTime)
		TmpShow=Format_Char_Show.Show_Char(ResultSum+"Time:"+OPTime,0)
		WriteSourceLog(TmpShow)
	print TmpShow
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

def Excute_cmd_root(s,Port,username,Password,Passwordroot,cmd,UseLocalScript,OPTime):
	global All_Servers_num_all,All_Servers_num,All_Servers_num_Succ,Done_Status,bufflog,FailIP,PWD
	PWD=re.sub("/{2,}","/",PWD)
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
                        t.connect(s,Port,username,pkey=key) 
                else:
			t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			t.connect(s,Port,username,Password)
		ssh=t.invoke_shell()
		ssh.send("LANG=zh_CN.UTF-8\n")
		ssh.send("export LANG\n")
		if username=='root':
			print "不能用root切换su-root"
			sys.exit()
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
				break
			else:
				if re.search('# *$',buff1):
					Result_status=True
        	       	 		All_Servers_num_Succ+=1
					break
		if Result_status:
			ssh.send("%s\n" % (PWD+cmd))
			buff=""
			bufflog=''
			while not buff.endswith("# "):
				resp=ssh.recv(9999)
				buff  += resp
				bufflog  += resp.strip('\r\n') + '\\n'
			t.close()
			All_Servers_num += 1
			buff='\n'.join(buff.split('\r\n')[1:][:-1])
			ResultSum=buff + "\n\033[1m\033[1;32m+OK [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m\n" % (username,s,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
			
			bufflog_new=''
			for t in bufflog.split():
				if t==cmd:
					continue
				bufflog_new+=t
			bufflog=bufflog_new
		else:
			All_Servers_num += 1
			FailIP.append(s)
			#buff=''.join(buff.split('\r\n')[:-1])+'\n'
			buff=''
			
			ResultSum=buff + "\n\033[1m\033[1;31m-ERR Su Failed (Password Error) [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m\n" % (username,s,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
			
	except Exception,e:
		All_Servers_num += 1
		Result_status=False
		FailIP.append(s)
		ResultSum="\n\033[1m\033[1;31m-ERR %s [%s@%s] (%0.2f Sec %d/%d)\033[1m\033[0m\a"   % (e,username,s,float(time.time() - start_time),All_Servers_num,All_Servers_num_all)
		bufflog=str(e)
	if Result_status:
		Write_Log(s,'NULL',bufflog.strip('\\n') + '\n',cmd,LogFile,'Y',username,UseLocalScript,'N','N',OPTime)
		TmpShow=Format_Char_Show.Show_Char(ResultSum+"Time:"+OPTime,0)
		WriteSourceLog(TmpShow)
	else:
		Write_Log(s,bufflog.strip('\\n'),'NULL\n',cmd,LogFile,'Y',username,UseLocalScript,'N','N',OPTime)
		TmpShow=Format_Char_Show.Show_Char(ResultSum+"Time:"+OPTime,0)
		WriteSourceLog(TmpShow)
	print TmpShow
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
	global All_Servers_num_all,All_Servers_num,All_Servers_num_Succ,Done_Status,Logcmd,ListenLog,Global_start_time,PWD,FailIP,ScriptFilePath,CONFMD5,HOSTSMD5
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
	elif sudo:
		CmdPrompt="CheungSSH sudo"
	else:
		CmdPrompt="CheungSSH"
	while True:
		All_Servers_num_all=len(Servers_T)
		OPTime=time.strftime('%Y%m%d%H%M%S',time.localtime())
		Askreboot="no"
		for t in threading.enumerate():
			if t is threading.currentThread():
				continue
			else:
				t.join()
		#Threading Done
		try:
			if IS_PWD:
				ShowPWD=re.sub(";$","",PWD.split()[1])
				ShowPWD=re.sub("/{2,}","/",ShowPWD)
				ShowPWD=re.sub("cd *","",ShowPWD)
			else:
				ShowPWD=re.sub(";$|cd *","",PWD)
		except Exception,e:
			ShowPWD=PWD
		cmd=raw_input("%s %s>>>> " % (CmdPrompt,ShowPWD  ))
		if HOSTSMD5!=filemd5.main(HostsFile):
			Askreboot=raw_input("Hosts配置文件发生变化,重启程序[%s]才能生效 (yes/no)? " %sys.argv[0])
			HOSTSMD5=filemd5.main(HostsFile)
		elif CONFMD5!=filemd5.main(ConfFile):
			Askreboot=raw_input("conf配置文件发生变化,重启程序[%s]才能生效 (yes/no)? " %sys.argv[0])
			CONFMD5=filemd5.main(ConfFile)
		if re.search("^ *[Yy]([Ee][Ss])? *$",Askreboot):
			sys.exit()
		cmd=re.sub('^ *ll *','ls -l ',cmd)
		cmd=re.sub("^ *top","top  -b -d 1 -n 1 ",cmd)
		cmd=re.sub("^ *ping","ping  -c 4 ",cmd)
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
					if not os.path.isfile("%s/cheung/flag/.NoAsk"%HOME):
						AskNotice=raw_input("\033[1;33m注意: 请您确保切换的路径[%s]在远程服务器上是存在的，否则切换路径没有任何意义,您清楚了吗？\033[0m(yes/no) " % (re.sub("^ *cd *|;","",PWD)))
						if re.search("[Yy]([Ee][Ss])?",AskNotice):
							AskCancel=raw_input("是否取消以上提示？(yes/no) ")
							if re.search("[Yy]([Ee][Ss])?",AskCancel):
								try:
									os.mknod("%s/cheung/flag/.NoAsk"%HOME)
									os.system("chmod 777 %s/cheung/flag/.NoAsk"%HOME)
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
		if re.search("^ *[Rr][Uu][Nn] +",cmd):
			try:
				#ScriptFilePath=cmd.split()[1:]
				ScriptFileCMD=cmd.split()[1:]
				IsScript=False
				for a in ScriptFileCMD:
					if os.path.isfile(a):
						ScriptFilePath=a
						IsScript=True
						break
				if not IsScript:
					print "您指定的脚本在您的本地不存在!"
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
					#Newcmd="""chmod a+x %s;%s;rm -f %s""" %(d_file,d_file,d_file)
					ScriptFileCMD=re.sub(ScriptFilePath,d_file,' '.join(ScriptFileCMD))
					Newcmd="""chmod a+x %s;%s;rm -f %s""" %(d_file,ScriptFileCMD,d_file)
					UseLocalScript="Y"
					Logcmd=ScriptFileCMD
			except IndexError:
				print "您尚未指定本服务器上的脚本路径 用法: run /path/scriptfile"
				continue
		else:
			UseLocalScript="N"
			Newcmd=cmd
			Logcmd=cmd

		if re.search("^ *[Ee][Xx][Ii][Tt] *$",cmd):
			sys.exit(0)
		if re.search("^ *[Cc][Ll][Ee][Aa][Rr] *",cmd):
			os.system("clear")
			continue
		if re.search('^ *[Ff][Ll][Uu][Ss][Hh] *[Ll][Oo][Gg][Ss] *$',cmd):
			try:
				Log_Flag=time.strftime('%Y%m%d%H%M%S',time.localtime())
				shutil.move('%s/cheung/logs/cheungssh.log'%HOME,'%s/cheung/logs/cheungssh%s.log' % (Log_Flag,HOME))
				print "+OK"
				continue
			except Exception,e:
				print "Waring : %s Failed (%s)" % (cmd,e)
				continue
		if re.search("^ *$",cmd):
			continue
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
					T=re.search("[Ff][Aa][Ii][Ll] *",SelectFailIP)
					if T:
						if not FailIP:
							print "当前没有执行命令失败的主机,无法选定"
						else:
							Servers_T=FailIP
							print "已选定执行命令[%s]失败的主机%s" %(LastCMD,FailIP)
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
			elif re.search("^ *[Nn][Oo] +[Aa][Ll]{2} *$",cmd):
				Servers_T=Servers
				#UseSystem=False
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
			elif re.search("^ *[Nn][Oo] +[Aa]([Ll]{2})? *$",cmd):
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
		if re.search("^ *vim? +",cmd):
			try:
				EditFile=cmd.split()[1]
			except Exception,e:
				print "没有指定文件"
				continue
			if not os.path.isfile("%s/cheung/flag/.NoAskEdit"%HOME):
				AskEdit=raw_input("您当前要编辑远程服务器上的文件，编辑完成后，所有服务器上的[%s]都将是您本次编辑的内容且内容一样。您是否同意这样的行为(yes/no)? " %EditFile)
				if not re.search("^ *[Yy]([Ee][Ss])? *$",AskEdit):
					print "忽略本次操作[%s]"% cmd
					continue
				else:
					NoAskEdit=raw_input("是否取消以上提示(yes/no) ? ")
					if  re.search("^ *[Yy]([Ee][Ss])? *$",NoAskEdit):
						try:
							os.mknod("%s/cheung/flag/.NoAskEdit"%HOME)
							print "已取消"
						except Exception,e:
							print "取消失败 (%s)" % e
							
			try:
						
				FileFlag=EditFile +str(random.randint(999999999,999999999999))
				for a in Servers_T:
					if UseKey=='Y':
						IsEdit=GetFile.GetFile(a,ServersPort[a],ServersUsername[a],None,'Y',EditFile,FileFlag)
					else:
						IsEdit=GetFile.GetFile(a,ServersPort[a],ServersUsername[a],ServersPassword[a],'N',EditFile,FileFlag)
						
					break
				if IsEdit:
					print 'Editing...'
					ViFile="/tmp/" +os.path.basename(FileFlag)
					FileMD5=filemd5.main(ViFile)
					try:
						os.system("vi %s"%ViFile)
						if not FileMD5==filemd5.main(ViFile):
							os.system("clear")
							print "Updateing  [%s] ..." % EditFile
							#if SysVersion<2.6:
							if UseKey=='Y':
								for a in Servers_T:
									UpdateFile.UpdateFile(a,ServersPort[a],ServersUsername[a],None,'Y',ViFile,EditFile)
							else:
								for a in Servers_T:
									UpdateFile.UpdateFile(a,ServersPort[a],ServersUsername[a],ServersPassword[a],'N',ViFile,EditFile)
								
									
									
					except Exception,e:
						print "编辑文件失败"
			except Exception,e:
				print "操作失败: ",e
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
						if sudo:
							a=threading.Thread(target=Excute_sudo,args=(s,ServersPort[s],ServersUsername[s],ServersPassword[s],Newcmd,UseLocalScript,OPTime))
						else:
							a=threading.Thread(target=SSH_cmd,args=(s,ServersUsername[s],None,ServersPort[s],Newcmd,UseLocalScript,OPTime))
					else:
						if sudo:
				
							a=threading.Thread(target=Excute_sudo,args=(s,ServersPort[s],ServersUsername[s],ServersPassword[s],Newcmd,UseLocalScript,OPTime))
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
					if sudo:
						Excute_sudo(s,ServersPort[s],ServersUsername[s],        ServersPassword[s],Newcmd,UseLocalScript,OPTime)
					else:
						SSH_cmd(s,ServersUsername[s],ServersPassword[s],ServersPort[s],Newcmd,UseLocalScript,OPTime)
							
			############################################################################################
if  __name__=='__main__':
	Read_config()
	Main_p()
