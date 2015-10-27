#!/usr/bin/env python
#coding:utf-8
from django.core.cache import cache
def gethostconf(id):
	hostconf=cache.get("host:%s"% id)
	return hostconf
