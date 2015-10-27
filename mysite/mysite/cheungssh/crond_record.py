#/usr/bin/evn python
#coding:utf-8
import os,sys,commands,json
sys.path.append('/home/cheungssh/mysite')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.core.cache import cache
crond_file="/home/cheungssh/crond/crond_file"
def crond_del(fid):
	crondlog_show=cache.get('crondlog')
	if crondlog_show:
		del_crond_file=commands.getstatusoutput("""sed -i  '/%s/d' %s  && /usr/bin/crontab  %s"""%(fid,crond_file,crond_file))
		if int(del_crond_file[0])==0:
			try:
				del crondlog_show[fid]
			except KeyError:
				pass
			except Exception,e:
				return True,False,str(e)
			cache.set('crondlog',crondlog_show,36000000000)
			return True,"OK"
		else:
			return False,del_crond_file[1]
	else:
		return False,"信息不存在"
def crond_record(value):
	fid=value.keys()[0]
	crondlog_source=cache.get('crondlog')
	allconf=cache.get('allconf')
	if crondlog_source:
		try:
			crondlog_source[value.keys()[0]]=value.values()[0]
			print '已经添加了日志'
		except Exception,e:
			print "发送错误",e
	else:
		print '没有日志'
		crondlog_source=value
	
	try:
		if allconf is None:
			print "没有配置"
		else:
			allconf_t=allconf['content']
		id=crondlog_source[fid]['id']
		ip=allconf_t[id]['ip']
	except Exception,e:
		ip="IP不存在"
		print "错误 ",e
	crondlog_source[fid]['ip']=ip
	if cache.set("crondlog",crondlog_source,3600000000):
		print '已经写入日志'
		return  True
	else:
		print '写入日志失败了'
		return False
def crond_show():
	crondlog_show=cache.get('crondlog')
	if crondlog_show:
		crondlog_show_all=crondlog_show
		for fid in crondlog_show_all.keys():
			fid_progres_info=cache.get('info:%s' % (fid))
			if fid_progres_info:
				crondlog_show_all[fid]['status']=fid_progres_info['msgtype']
				try:
					crondlog_show_all[fid]['lasttime']=fid_progres_info['lasttime']
				except:
					pass
				if fid_progres_info['content']:
					crondlog_show_all[fid]['content']=fid_progres_info['content']
				else:
					crondlog_show_all[fid]['content']="正常"
		crondlog_show=crondlog_show_all.values()
		return True,crondlog_show
	else:
		return False,"没有任务"
