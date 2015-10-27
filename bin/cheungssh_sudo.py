#coding:utf8
#Author=Cheung Kei-Chuen
#QQ=2418731289
import paramiko,os,sys,re,Format_Char_Show_web,time,sendinfo,random,json

def Excute_sudo(ip,username,password,port,loginmethod,keyfile,cmd,ie_key,group,sudopassword,Data):
	bufflog=''
	start_time=time.time()
	ResultSum=''
	Result_status=False
	prompt='# '
	sudo="sudo su  - root"
	try:
		t=paramiko.SSHClient()
                if loginmethod=='KEY':
			KeyPath=os.path.expanduser(keyfile)
                        key=paramiko.RSAKey.from_private_key_file(KeyPath)
                        t.load_system_host_keys()
			t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        t.connect(ip,port,username,pkey=key) 
                else:
			t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			t.connect(ip,port,username,password)
		ssh=t.invoke_shell()
		ssh.send("LANG=zh_CN.US\n")
		ssh.send("export LANG\n")
		ssh.send("%s\n"%sudo)
		buff=''
		resp=''
		info=''
		EnterPassword=False
		color_status=1
		while True:
			print "当前值:",resp
			if re.search("\[sudo\] +password for.*:",resp):
				ssh.send("%s\n"%password)
				print "已经发送密码"
				while True:
					print '开始接受正式命令消息,下面在recv...'
					resp=ssh.recv(100)
					print 'recv 完毕..正在检查登录是否成功'
					if re.search("Sorry, try again",resp):
						EnterPassword=True
						print '密码错误'
						info='密码错误'
						break
					elif re.search('%s +.*sudoers'%username,resp):
						EnterPassword=True
						print '没有sudo权限'
						info="没有sudo权限"
						break
					elif resp.endswith(prompt):
						print "登录成功"
						EnterPassword=True
						Result_status=True
						color_status=0
						break
					else:
						print "消息是:",resp
			if EnterPassword:break
			if buff.endswith(prompt):
				Result_status=True
				color_status=0
				break
			if re.search('%s +.*sudoers'%username,resp):
				info="没有sudo权限"
				break
			resp=ssh.recv(9999)
			buff += resp
		if Result_status:
			print "登录成功"
			ssh.send("%s\n" % (cmd))
			buff=""
			bufflog=''
			while not buff.endswith(prompt):
				resp=ssh.recv(9999)
				buff  += resp
				bufflog  += resp.strip('\r\n') + '\\n'
			t.close()
			Data.All_Servers_num += 1
			buff='\n'.join(buff.split('\r\n')[1:][:-1])
			ResultSum=buff
			
			bufflog_new=''
			for t in bufflog.split():
				if t==cmd:
					continue
				bufflog_new+=t
			bufflog=bufflog_new
			Data.All_Servers_num_Succ+=1
		else:
			Data.All_Servers_num += 1
			Data.FailIP.append(ip)
			buff=''
			ResultSum=buff + "sudo %s" % (info)
		##################
		Show_Result_web_status=Format_Char_Show_web.Show_Char(ResultSum.replace("<","&lt;")+username+"@"+ip,color_status)
		Show_Result=ResultSum + '\n' #+ResultSum_count
		jindu=int(float(Data.All_Servers_num)/float(Data.All_Servers_num_all)*100)
		TmpShow=Format_Char_Show_web.Show_Char(Show_Result+" 命令: "+cmd,color_status)
		if color_status==1:
			info={"msgtype":1,"content":[{"group":group,"servers":[{"ip":username+"@"+ip,"status":"ERR","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		else:
			info={"msgtype":1,"content":[{"group":group,"servers":[{"ip":username+"@"+ip,"status":"OK","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		b_id=str(random.randint(999999999,99999999999999999))
		info["id"]=b_id
		info=json.dumps(info,encoding='utf8',ensure_ascii=False)
		#######	
	except Exception,e:
		print '链接服务器错误'
		color_status=1
		Data.All_Servers_num += 1
		Result_status=False
		Data.FailIP.append(ip)
		ResultSum=str(e)
		bufflog=str(e)
		TmpShow=Format_Char_Show_web.Show_Char(ResultSum,1)
		jindu=int(float(Data.All_Servers_num)/float(Data.All_Servers_num_all)*100)
		Show_Result_web_status=Format_Char_Show_web.Show_Char(str(e).replace("<","&lt;")+"\n"+username+"@"+ip,color_status)
		info={"msgtype":1,"content":[{"group":group,"servers":[{"ip":username+"@"+ip,"status":"ERR","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
		info['id']=(str(random.randint(999999999,99999999999999999)))
		info=json.dumps(info,encoding='utf8',ensure_ascii=False)
	#sendinfo.sendinfo(str({ie_key:info}))
	if Data.excutetype=='cmd':
		sendinfo.sendinfo(str({ie_key:info}))
		print '这是发送给socket'
        else:
		print '这是sudo'
		checktime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		hwinfo=cache.get('hwinfo')
		if not  hwinfo:
			hwinfo={}
			ipinfo={Data.hwtype:ResultSum,'ip':ip,'checktime':checktime}
			hwinfo[ip]=ipinfo
		else:
			#hwinfo[ip][Data.hwtype]=ResultSum
			if hwinfo.has_key(ip):
				hwinfo[ip][Data.hwtype]=ResultSum
			else:
				ipinfo={Data.hwtype:ResultSum,'ip':ip,'checktime':checktime}
				hwinfo[ip]=ipinfo
				hwinfo[ip][Data.hwtype]=ResultSum
				
		cache.set('hwinfo',hwinfo,864000000)
