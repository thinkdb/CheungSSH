#!/usr/bin/python
#coding:utf-8
import sys
print "Content-Type: text/html\n"
try:
	import MySQLdb,json
except Exception,e:
	print 'Err'
	sys.exit(1)
server_group={"type":"group","content":[]}
try:
	conn=MySQLdb.connect(user='root',passwd='zhang',db='cheungssh')
	cursor=conn.cursor()
	cursor.execute("select  * from cheungssh_serverconf")
	for a in  cursor.fetchall():
		id=a[0]
		IP=a[1]
		Port=a[2]
		Group=a[3]
		Username=a[4]
		Password=a[5]
		KeyFile=a[6]
		Sudo=a[7]
		SudoPassword=a[8]
		Su=a[9]
		SuPassword=a[10]
		LoginMethod=a[11]
		if not Group in server_group["content"]:server_group["content"].append(Group)
	conn.close()
	
except Exception,e:
	print 'Err',e
	sys.exit(1)
server_group=json.dumps(server_group,encoding="utf8",ensure_ascii=False)
print server_group
