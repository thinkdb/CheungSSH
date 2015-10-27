#coding:utf-8
import os,sys,time,paramiko,Format_Char_Show_web,re,random,json,sendinfo
def Excute_suroot(ip,username,password,port,loginmethod,keyfile,cmd,ie_key,group,rootpassword,Data):
	bufflog=''
	start_time=time.time()
	ResultSum=''
	Result_status=False
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
		ssh.send("LANG=zh_CN.UTF-8\n")
		ssh.send("export LANG\n")
		ssh.send("su - root\n")
		buff=''
		while not re.search("Password:",buff) and not re.search("：", buff):
			resp=ssh.recv(9999)
			buff += resp
		ssh.send("%s\n" % (rootpassword))
		buff1=''
		while True:
			resp=ssh.recv(500)
			buff1 += resp
			if  re.search('su:',buff1):
				break
			else:
				if re.search('# *$',buff1):
					color_status=0
					Result_status=True
        	       	 		Data.All_Servers_num_Succ+=1
					break
		if Result_status:
			print 'su是正确的'
			color_status=0
			ssh.send("%s\n" % (cmd))
			buff=""
			bufflog=''
			while not buff.endswith("# "):
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
		else:
			print 'su失败的'
			color_status=1
			Data.All_Servers_num += 1
			Data.FailIP.append(ip)
			buff=''
			
			ResultSum=buff + "Su Failed (Password Error)"
		print 'color:',color_status
		Show_Result_web_status=Format_Char_Show_web.Show_Char(ResultSum.replace("<","&lt;")+username+"@"+ip,color_status)
		print 'color:',color_status
			
	except Exception,e:
		color_status=1
		Data.All_Servers_num += 1
		Result_status=False
		Data.FailIP.append(ip)
		ResultSum=str(e)
		bufflog=str(e)
		Show_Result_web_status=Format_Char_Show_web.Show_Char(str(e).replace("<","&lt;")+"\n"+username+"@"+ip,color_status)
	jindu=int(float(Data.All_Servers_num)/float(Data.All_Servers_num_all)*100)
	if color_status==0:
		info={"msgtype":1,"content":[{"group":group,"servers":[{"ip":username+"@"+ip,"status":"OK","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
	else:
		info={"msgtype":1,"content":[{"group":group,"servers":[{"ip":username+"@"+ip,"status":"ERR","jindu":jindu,"cmd":cmd,"info":Show_Result_web_status}]}]}
	info['id']=(str(random.randint(999999999,99999999999999999)))
	info=json.dumps(info,encoding='utf8',ensure_ascii=False)
	#sendinfo.sendinfo(str({ie_key:info}))
	if Data.excutetype=='cmd':
		sendinfo.sendinfo(str({ie_key:info}))
	else:
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
