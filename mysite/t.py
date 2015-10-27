#!/usr/bin/python
#coding:utf-8
import redis,re
r=redis.StrictRedis(host='localhost', port=6379, db=0, password='testpassword')
c=r.get(':1:host:4')
print eval(re.search('{.*}',c).group())["port"]
