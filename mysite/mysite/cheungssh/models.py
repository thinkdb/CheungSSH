#coding:utf-8
# Create your models here.
from django.db import models


class Main_Conf(models.Model):
	runmod_choices=(("M","多线程"),("S","单线程"))
	RunMode=models.CharField(max_length=1,choices=runmod_choices)
	TimeOut=models.IntegerField(max_length=5)
	class Meta:
		permissions=(
				("edit","编辑权限"),
				("show","查看权限"),
			)
class ServerConf(models.Model):
	sudo_choices=( ("Y","使用sudo登陆"),("N","普通登陆")    )
	su_choices=( ("Y","su - root 登陆"),("N","普通登陆")    )
	login_type=(   ("KEY","使用PublickKey登陆"),("PASSWORD","使用密码登陆")  )
	IP=models.CharField(max_length=200)
	HostName=models.CharField(max_length=100,null=False,blank=False)
	Port=models.IntegerField(max_length=5)
	Group=models.CharField(max_length=200,null=False,verbose_name="主机组")   #verbose_name 显示成中文
	Username=models.CharField(max_length=200,null=False)
	Password=models.CharField(('password'),max_length=128)
	#KeyFile=models.FileField(upload_to="keyfile",default="N")
	KeyFile=models.CharField(max_length=100,default="N")
	Sudo=models.CharField(max_length=1,choices=sudo_choices,default="N")
	SudoPassword=models.CharField(max_length=2000,null=True,blank=True)
	Su=models.CharField(max_length=1,choices=su_choices,null=True,blank=True,default="N")
	SuPassword=models.CharField(max_length=2000,null=True,blank=True,default="N")
	LoginMethod=models.CharField(max_length=10,choices=login_type,null=True,blank=True,default="N")
	class Meta:
		permissions=(
				("edit","编辑权限"),
				("show","查看权限"),
			)
	def __unicode__(self):
		return self.IP
	
class ServerInfo(models.Model):
	IP=models.OneToOneField(ServerConf)  #这里应该是一对一的关系，如果是多对多， 在web页面上的显示逻辑就是一个文本框包含了全部IP，而如果用OneToOne的关系就是一个对应一个，IP那里就变成了下拉选择IP了
	Position=models.TextField(null=True,blank=True)
	Description=models.TextField(null=True,blank=True,default="请在这里写一个对服务器的描述")
	CPU=models.CharField(max_length=20,default="暂无",null=True,blank=True)
	CPU_process_must=models.CharField(max_length=10,default="暂无",null=True,blank=True)
	MEM_process_must=models.CharField(max_length=10,default="暂无",null=True,blank=True)
	Use_CPU=models.CharField(max_length=20,default="暂无",null=True,blank=True)
	uSE_MEM=models.CharField(max_length=20,default="暂无",null=True,blank=True)
	MEM=models.CharField(max_length=20,default="暂无",null=True,blank=True)
	IO=models.CharField(max_length=200,default="暂无",null=True,blank=True)
	Platform=models.CharField(max_length=200,default="暂无",blank=True)
	System=models.CharField(max_length=200,default="暂无",blank=True)
	InBankWidth=models.IntegerField(max_length=20,null=True,blank=True)
	OutBankWidth=models.IntegerField(max_length=20,null=True,blank=True)
	CurrentUser=models.IntegerField(max_length=10,null=True,blank=True)
	def __unicode__(self):
		return self.Position
	
	
	
	




#from django.contrib.auth.models import User   #这个是用外键关联django自带的User表
"""class BBS(models.Model):
	title=models.CharField(max_length=64)
	summary=models.CharField(max_length=256,null=True,null=True) # 表里为空是null=True
	content=models.TextField()
	author=models.ForeignKey('BBS_user')
	view_count=models.IntegerField()
	ranking=models.IntegerField()
	created_at=models.DateTimeField()
	choices_show=(  ("N","不显示"),("Y","显示")  )
	show_is=models.CharField(max_length=2,choices=choices_show)
	def  __unicode__(self):
		return self.title  #这里返回的字段多少咩有任何影响，在做前台显示的时候， 这个是没有影响的一样可以通过  [.字段名]的形式返回值
		# 这里的return只是一个默认的字段而已， 在django中，可以用这个这样的方式访问该表里面的其他字段，比如 title.content
	class Admin:
		pass
class Gategory(models.Model):
	name=models.CharField(max_length=32,unique=True)  #unique表示不重复
	administrator=models.ForeignKey('BBS_user')
class BBS_user(models.Model):
	#user=models.CharField(max_length=20)
	user=models.OneToOneField(User)
	singnature=models.CharField(max_length=128,default="太懒了，什么都没写")
	photo=models.ImageField(upload_to="imgs",default="default.png")
	def __unicode__(self):
		return self.user.username
		#return self.user #注意，下面这种返回方式是错误的，否则会遇到User Fond的错误"""

