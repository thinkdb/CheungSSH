#coding:utf-8
def hwinfo(cache):
	info=[]
	t_hwinfo=cache.get('hwinfo')
	if t_hwinfo:
		info=t_hwinfo.values()
	return info
	
	
