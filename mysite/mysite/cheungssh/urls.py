#coding:utf-8
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from mysite.cheungssh.cheungssh import cheungssh_index
#from mysite.cheungssh.cheungssh import test
import mysite
urlpatterns = patterns('',
	url(r'^cheungssh/login/$','mysite.cheungssh.cheungssh.cheungssh_login'),
	url(r'^cheungssh/logout/$','mysite.cheungssh.cheungssh.cheungssh_logout'),
	#url(r'^cheungssh/test/$',mysite.cheungssh.cheungssh.test.as_view()), #类视图
	#url(r'^cheungssh/test/test/$','mysite.cheungssh.cheungssh.haha'), #类视图
	url(r'^cheungssh/t/$','mysite.cheungssh.cheungssh.t1'), #类视图
	url(r'^cheungssh/sshcheck/$','mysite.cheungssh.cheungssh.sshcheck'), #类视图
	#url(r'^cheungssh/test/test/test/$','mysite.cheungssh.test.haha'), #类视图
	#url(r'^cheungssh/test/test/test/ha$','mysite.cheungssh.test.hahaha'), #类视图
	url(r'^cheungssh/excutecmd/$','mysite.cheungssh.cheungssh.excutecmd'),
	url(r'^cheungssh/cmdhistory/?$','mysite.cheungssh.cheungssh.cmdhistory'),
	url(r'^cheungssh/upload/test/$','mysite.cheungssh.cheungssh.upload_file_test'),
	url(r'^cheungssh/download/$','mysite.cheungssh.cheungssh.download_file'),
	url(r'^cheungssh/pathsearch/$','mysite.cheungssh.cheungssh.pathsearch'),
	url(r'^cheungssh/configmodify/$','mysite.cheungssh.cheungssh.configmodify'),
	url(r'^cheungssh/crontab/$','mysite.cheungssh.cheungssh.crontab'),
	url(r'^cheungssh/showcrondlog/$','mysite.cheungssh.cheungssh.showcrondlog'),
	url(r'^cheungssh/delcrondlog/$','mysite.cheungssh.cheungssh.delcrondlog'),
	url(r'^cheungssh/delkey/$','mysite.cheungssh.cheungssh.delkey'),
	url(r'^cheungssh/keyadmin/$','mysite.cheungssh.cheungssh.keyshow'),
	url(r'^cheungssh/local_upload_show/$','mysite.cheungssh.cheungssh.local_upload_show'),
	url(r'^cheungssh/$',cache_page(cheungssh_index,30*1)),
	url(r'^cheungssh/hostinfo/$','mysite.cheungssh.hostinfo.hostinfo'),
	url(r'^cheungssh/translog/$','mysite.cheungssh.hostinfo.translog'),
	url(r'^cheungssh/groupinfo/$','mysite.cheungssh.hostinfo.groupinfo'),
	url(r'^cheungssh/groupinfoall/$','mysite.cheungssh.hostinfo.groupinfoall'),
	url(r'^cheungssh/progres/$','mysite.cheungssh.hostinfo.get_progres'),
	url(r'^cheungssh/filetrans/$','mysite.cheungssh.cheungssh.filetrans'),
	url(r'^cheungssh/hwinfo/$','mysite.cheungssh.cheungssh.get_hwinfo'),
	url(r'^cheungssh/script/$','mysite.cheungssh.cheungssh.get_script'),
	url(r'^cheungssh/operationrecord/$','mysite.cheungssh.cheungssh.operation_record'),
	#url(r'^cheungssh/cache/$',cache_page(cache_test,60*1)),
	)
