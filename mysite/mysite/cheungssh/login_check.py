#coding:utf-8
import time,IP,json
from django.core.cache import cache
from django.http import HttpResponse
#def login_check(request,isRecord=True):
def login_check(isRecord=True):
	def decorator(func):
		def login_auth_check(request,*args,**kws):
			callback=request.GET.get('callback')
			info={}
			info['accesstime']=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
			info['URL']=  "%s?%s"   %(request.META['PATH_INFO'],request.META['QUERY_STRING'])
			info['IP']=request.META['REMOTE_ADDR']
			info['IPLocat']=IP.find(info['IP'])
			isAuth=False #默认为认证不通过，简化下面else的重写
			if request.user.is_authenticated():
				info["username"]=request.user.username
				isAuth=True
			else:
				info["username"]="非认证用户"
			#####写入redis ,该值为list，因为username是重复的， 如果用dict，记录会被覆盖
			login_record=cache.get('login_record')
			if login_record:
				login_record.append(info)
			else:
				login_record=[info]
			if isRecord:
				cache.set('login_record',login_record,86400000) #写入redis
			#####写入redis
			if isAuth:
				return func(request,*args,**kws)
			else:
				backinfo={'msgtype':'login'}#重写信息，该信息是返回给web的，不影响后台的info记录
				backinfo=json.dumps(backinfo)
				if callback:
					info="%s(%s)"  % (callback,backinfo)
				else:
					info="%s"  % (backinfo)
				return HttpResponse(info)
			
		return login_auth_check
	return decorator
