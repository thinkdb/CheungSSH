#!/bin/bash
if [ ! -f ~/cheung/flag/installed ]
then
	echo "尚未安装程序，请执行install-ChuengSSH.sh安装!"
	exit 1
fi
mkdir -p ~/cheung/pid
ip=`ifconfig |grep -v 'inet6'|grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' -o|grep -vE '^(127|255)|255$'|head -1`
ls ~/cheung/bin/websocket_server_cheung.py >/dev/null 2>&1
if [ $? -ne 0 ]
then
        echo "您的~/cheung/bin目录没有CheungSSH web启动程序，请cd切换到目标路径后再行启动本程序!"
        exit 1
fi
start(){
	pid=`cat ~/cheung/pid/cheungssh.pid 2>/dev/null`
	kill -9 $pid 2>/dev/null
	netstat -anlut|grep  '0.0.0.0:1337' -q
	if  [ $? -eq 0 ]
	then
		echo "无法终止残余进程，请手动清除1337端口所在进程"
		exit 1
	else
		echo "已停止"
	fi
	echo  "正在启动..."
	nohup python websocket_server_cheung.py >>~/cheung/logs/web_run.log  2>&1 &
	if [ $? -ne 0 ]
	then
		echo "启动web系统失败！请检查原因"
	else
		echo  -e "已经启动Cheung Web系统请,打开浏览器访问:\n\thttp://$ip/cheungssh/index.html"
		echo "重要提示:本程序是cheungssh服务器程序，您要访问网页，请先确保您有http服务存在！否则是无法访问网页的"
	fi
	echo  "$!" >~/cheung/pid/cheungssh.pid
	now_md5=`md5sum ~/cheung/conf/hosts|awk '{print  $1}'`
	cat ~/cheung/flag/check.pid 2>/dev/null|xargs  -i kill  -9 {} 2>/dev/null
	while [ 1 ]
	do
		t_md5=`md5sum ~/cheung/conf/hosts|awk '{print  $1}'`
		if [ ${now_md5} != ${t_md5} ]
		then
			python ~/cheung/bin/sendinfo.py '<script type="text/javascript">alert("系统检测到配置文件发生变化，请您手动重启 ~/cheung/bin/web_server.sh restart")</script>' >/dev/null
			cat <<EOFsend|python
import sendinfo,get_info
info={"""all""":"""%s"""% (str(get_info.get_info(2)))}
info=str(info)
sendinfo.sendinfo(info)
EOFsend
		now_md5=$t_md5
		fi
		sleep 1
	done &
	echo  $! >~/cheung/flag/check.pid
}
status(){
	pid=`cat ~/cheung/pid/cheungssh.pid 2>/dev/null`
	if [ ! -z $pid ] && [ `ps -fel|awk  -v pid=$pid  '{if($4==pid){print "yes";exit}}'` == "yes" ]
	then
		echo "CheungSSH Web pid($pid)  is running ..."
		exit 0
	else
		echo "No runing"
		exit 2
	fi
	
}
case $1 in
	start)
		start
	;;
stop)
        pid=`cat ~/cheung/pid/cheungssh.pid 2>/dev/null`
        kill -9 $pid 2>/dev/null
	netstat -anlut|grep  '0.0.0.0:1337' -q
        if  [ $? -eq 0 ]
        then
                echo "无法终止残余进程，请手动清除1337端口所在进程"
                exit 1
        else
                echo "已停止"
        fi
	;;
	status)
		status
		;;
restart)
	start
	;;
	*)
		echo "Useage: $0 {start|stop|restart}"""
		exit 1
esac
