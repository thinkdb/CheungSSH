#!/bin/bash
setenforce 0
start(){
	service httpd stop &&
	service mysqld stop
	if [ $? -ne 0 ]
	then
		echo "停止程序失败，请检查原因"
		exit 1
	fi
	killall  -9 httpd
	killall  -9 redis-server 2>/dev/null
	netstat -anplut|grep '0.0.0.0:1337'|awk   '{split($NF,A,"/") ;print A[1]}' |xargs kill  -9 {} 2>/dev/null
	netstat -anplut|grep  '0.0.0.0:1337' -q
	if  [ $? -eq 0 ]
	then
		echo "无法终止残余进程，请手动清除1337端口所在进程"
		exit 1
	else
		echo "已停止"
	fi
	echo  "正在启动..."
	nohup python /home/cheungssh/bin/websocket_server_cheung.py >>/home/cheungssh/logs/web_run.log  2>&1 &
	if [ $? -ne 0 ]
	then
		echo "启动web系统失败！请检查原因"
		exit 1
	fi
	service mysqld start &&
	/home/cheungssh/redis-3.0.4/src/redis-server /home/cheungssh/conf/redis.conf   &&
	service httpd start  &&
	if [ $? -ne 0 ]
	then
		echo  "启动以上服务失败，请检查原因"
		exit 1
	else
		echo "已启动CheungSSH"
	fi
}
status(){
	pid=`netstat -anplut|grep '0.0.0.0:1337'|awk   '{split($NF,A,"/") ;print A[1]}'`
	if  [[ ! -z $pid ]]
	then
		echo "CheungSSH Web pid($pid)  is running ..."
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
	service httpd stop &&
	service mysqld stop
	if [ $? -ne 0 ]
	then
		echo "停止程序失败，请检查原因"
		exit 1
	fi
	killall  -9 httpd
	killall  -9 redis-server 2>/dev/null
	netstat -anplut|grep '0.0.0.0:1337'|awk   '{split($NF,A,"/") ;print A[1]}' |xargs kill  -9 {} 2>/dev/null
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
