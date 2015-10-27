#coding:utf-8
from django.http import  HttpResponse
def go(a='meiyou'):
	def decorator(func):
		def haha(request,*args,**kws):
			return HttpResponse(a)
		return haha
	return decorator

