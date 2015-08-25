#!/bin/bash
if [ ! -f ~/cheung/flag/installed ]
then
	echo "尚未安装程序，请执行install-ChuengSSH.sh安装!"
	exit 1
fi
#python ~/cheung/bin/sendinfo.py '<script type="text/javascript">alert("系统将立即重启!")</script>' >/dev/null
ps -fel|grep websocket_server_cheung.py|grep  -v "$$"|awk  '{print  $4}'|xargs -i kill  -9 {}
netstat -anlut|grep LISTEN|awk  '$4~"1337"{system("echo 有残余进程;killall  -9 python")}'
ls ~/cheung/bin/websocket_server_cheung.py >/dev/null 2>&1
if [ $? -ne 0 ]
then
	echo "您的~/cheung/bin目录没有CheungSSH web启动程序，请cd切换到目标路径后再行启动本程序!"
	exit 1
fi 
ip=`ifconfig |grep -v 'inet6'|grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' -o|grep -vE '^(127|255)|255$'|head -1`
python ~/cheung/bin/cheungssh_web.py "id -u" "all"
if [ $? -ne 0 ]
then
	echo "有报错，您的CheungSSH没有正确配置，无法启动web系统"
	exit 1
else
	nohup python websocket_server_cheung.py >>~/cheung/logs/web_run.log  2>&1 &
	if [ $? -ne 0 ]
	then
		echo "启动web系统失败！请检查原因"
	else
		echo  -e "已经启动Cheung Web系统请,打开浏览器访问:\n\thttp://$ip/cheungssh/index.html"
		echo "重要提示:本程序是cheungssh服务器程序，您要访问网页，请先确保您有http服务存在！否则是无法访问网页的"
	fi
fi
now_md5=`md5sum ~/cheung/conf/hosts|awk '{print  $1}'`

cat ~/cheung/flag/check.pid 2>/dev/null|xargs  -i kill  -9 {} 2>/dev/null
while [ 1 ]
do
	t_md5=`md5sum ~/cheung/conf/hosts|awk '{print  $1}'`
	if [ ${now_md5} != ${t_md5} ]
	then
		python ~/cheung/bin/sendinfo.py '<script type="text/javascript">alert("系统检测到配置文件发生变化，请您手动重启~/cheung/bin/start_CheungSSH_web.sh")</script>' >/dev/null
		now_md5=$t_md5
	fi
	sleep 2
done &
echo  $! >~/cheung/flag/check.pid
	
	
