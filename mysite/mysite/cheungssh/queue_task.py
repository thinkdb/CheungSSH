#!/usr/bin/env python
#coding:utf-8
import redis
r = redis.Redis(host='localhost', port=6379, db=0,password='testpassword')
def queuq_task(v,k='keylog'):
	r.lpush(k,v)
