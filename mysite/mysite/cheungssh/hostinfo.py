#coding:utf-8
import commands
import json
from django.http import HttpResponse
from mysite.cheungssh.models import ServerConf
from django.core.cache import cache
import login_check
@login_check.login_check()
def hostinfo(request):
	callback=request.GET.get('callback')
	group=request.GET.get('group')
	hostinfo={"msgtype":"OK","content":[]}
	username=request.user.username
	group=request.GET.get('group')
	t_groupinfo=cache.get("allconf")
	if t_groupinfo:
		host_in_group=[]
                for a in t_groupinfo['content'].values():
			if a['group']==group:
				try:
					if a['owner']==username:
						host_in_group.append({"ip": "%s@%s" % (a['username'],a['ip']),"id":a["id"]})
				except KeyError:
					print '不存在所属用户'
					pass
		hostinfo['content']=host_in_group
	info=json.dumps(hostinfo,encoding='utf-8',ensure_ascii=False)
	if callback is None:
		backstr=info
	else:
		backstr="%s(%s)"  % (callback,info)
	return HttpResponse(backstr)
	
	
@login_check.login_check()
def get_progres(request):
	fid=request.GET.get('fid')
	callback=request.GET.get('callback')
	info={"msgtype":"OK","content":""}
	fid="info:%s"%(fid)
	t_info=cache.get(fid)
	if t_info is None:
		info["status"]="ERR"
		info['content']='No-exists'.decode('utf-8')
		print '不存在'
	else:
		info=t_info
	info=json.dumps(info)
	print info,11111111111111111111
	if callback is None:
		backstr=info
	else:
		backstr="%s(%s)"  % (callback,info)
	return HttpResponse(backstr)
@login_check.login_check()
def groupinfoall(request):
	callback=request.GET.get("callback")
	allconfinfo={"msgtype":"OK","content":{}}
	username=request.user.username
	t_allconfinfo=cache.get("allconf")
	if t_allconfinfo is None:
		data=ServerConf.objects.all()
		for a in data:
			t_host={}
			t_host["id"]=a.id
			t_host["su"]=a.Su
			t_host["group"]=a.Group
			t_host["ip"]=a.IP
			t_host["username"]=a.Username
			t_host["password"]=a.Password
			t_host["hostname"]=a.HostName
			t_host["port"]=int(a.Port)
			t_host["keyfile"]=a.KeyFile
			t_host["sudo"]=a.Sudo
			t_host["su"]=a.Su
			t_host["supassword"]=a.SuPassword
			#t_host["sudopassword"]=a.SudoPassword
			t_host["loginmethod"]=a.LoginMethod
			allconfinfo['content'][a.id]=t_host
			cache.set("allconf",allconfinfo,360000)
        else:
		for b in t_allconfinfo['content'].keys():
			t_allconfinfo['content'][b]['password']="**********"
			t_allconfinfo['content'][b]['supassword']="**********"
			#t_allconfinfo['content'][b]['sudopassword']="**********"
                allconfinfo=t_allconfinfo	
	#allconfinfo_web=allconfinfo['content'].values()
	allconfinfo_web=[]
	for a in allconfinfo['content'].values():
		try:
			if a['owner'] == username:
				allconfinfo_web.append(a)
		except KeyError:
			pass
		except Exception,e:
			info['content']=str(e)
	allconfinfo['content']=allconfinfo_web
	info=json.dumps(allconfinfo,encoding="utf8",ensure_ascii=False)
	if callback is None:
		backstr=info
	else:
		backstr="%s(%s)"  % (callback,info)
	return HttpResponse(backstr)
@login_check.login_check()
def groupinfo(request):
        groupinfo={"msgtype":"OK","content":[]}
        callback=request.GET.get("callback")
	username=request.user.username
        t_groupinfo=cache.get("allconf")
	if t_groupinfo:
		all_group=[]
		for a in t_groupinfo['content'].values():
			try:
				if a['owner']==username:
					all_group.append(a['group'])
			except KeyError:
				pass
			except Exception,e:
				print '错误',e
				groupinfo['content']=str(e)
		groupinfo['content']=list(set(all_group))
        info=json.dumps(groupinfo,encoding="utf8",ensure_ascii=False)
	if callback is None:
		backstr=info
	else:
		backstr="%s(%s)"  % (callback,info)
	return HttpResponse(backstr)


	

@login_check.login_check()
def translog(request):
	info={"msgtype":"OK",'content':""}
	callback=request.GET.get("callback")
	cache_translog=cache.get("translog")
	if not  cache_translog:
		cache_translog=[]
	info['content']=cache_translog
	info=json.dumps(info)
	if callback is None:
		backstr=info
	else:
		backstr="%s(%s)"  % (callback,info)
	return HttpResponse(backstr)
