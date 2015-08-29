#!/bin/bash
#Author=Cheung Kei-Chuen
#QQ=2418731289
#coding:utf-8
#如果您在使用过程中，遇到了一点点的问题，我都真诚希望您能告诉我！为了改善这个软件， 方便您的工作#
export LANG=zh_CN.UTF-8
if [ `id -u` -ne 0 ]
then
	echo "Must be as root install!"
	exit 1
fi
echo  "Installing..."
mkdir -p ~/cheung/
cat <<EOFver|python
#coding:utf-8
import sys,time
ver=float(sys.version[:3])
if ver<=2.4:
	print "强烈警告! 您使用的python版本过低,建议升级python版本到2.6以上.\n可以使用yum update python更新"
	time.sleep(3)
EOFver
##判断是否有paramiko
cat<<EOF|python
import sys
try:
        import paramiko
except AttributeError:
	 os.system("""sed  -i '/You should rebuild using libgmp/d;/HAVE_DECL_MPZ_POWM_SEC/d'  /usr/lib64/python*/site-packages/Crypto/Util/number.py       /usr/lib/python*/site-packages/pycrypto*/Crypto/Util/number.py""")
except:
        sys.exit(1)
EOF
if [ $? -ne 0 ]
then
	
	rpm  -qa|grep gcc -q
	if  [ $? -ne 0 ]
	then
        	echo  "您的系统当前没有gcc环境！,请执行: yum  install -y gcc  安装！"
		exit
	fi
	rpm  -qa|grep python-devel -q
	if [ $? -ne 0 ]
	then
		echo "您的系统没有python-devel包，请手动执行: yum install -y python-devel  安装！"
		exit
	fi
        echo "当前没有paramiko"
	cat<<EOFcrypto|python
import sys
try:
	import Crypto
except:
	sys.exit(1)
EOFcrypto
	if [ $? -ne 0 ]
	then
		echo "没有crypto，现在需要安装"
		cd ../soft
		tar xf pycrypto-2.6.1.tar.gz
		cd pycrypto-2.6.1
		python setup.py  install
		if  [ $? -ne 0 ]
		then
			echo "安装pycropto失败，请检查系统是否有GCC编译环境,如果没有gcc环境，请安装: yum  install -y gcc 或者联系Q群:456335218"
			exit
		else
			echo "安装pycropto完成"
			cd ../../bin
		fi
	fi
	echo "开始安装paramiko..."
	cd ../soft
	tar xf paramiko-1.9.0.tar.gz
	cd paramiko-1.9.0
	python setup.py install
	if [ $? -ne 0 ]
	then
		echo "安装paramiko失败，请检查系统是否有gcc环境和python-devel环境，或者联系Q群：456335218"
	else
		echo "安装paramiko完成"
		cd ../../bin
	fi
else
	echo "paramiko已经就绪"
fi
####
cat<<EOFjson|python
#coding:utf-8
import sys
try:
	import json
except:
	sys.exit(1)
EOFjson
if  [ $? -ne 0 ]
then
	echo -e "系统没有json模块，您需要安装json模块!如果您的服务器版本比较低，比如5.5版本以下，那么安装json很可能是困难的,建议您换一个高版本的服务器,如果可以您也可以尝试手动安装json模块\n或者您可以通过更新python版本解决 yum update python"
	echo -e  "警告:\n\t没有json模块的情况下，无法启动web系统!但您可以使用shell版本的CheungSSH\n\t如果您要使用web版本，必须安装json模块"
	read -p "按下Enter继续..." t_tmp
fi
####

cat<<EOFhashlib|python
import sys
try:
	import hashlib
except:
	sys.exit(1)
EOFhashlib
if [ $? -ne 0 ]
then
	echo "系统没有hashlib,正在安装"
	cd ../soft/
	unzip  hashlib-20081119.zip
	cd hashlib-20081119
	python setup.py install
	if [ $? -ne 0 ]
	then
		echo "安装hashlib失败，请检查系统环境"
		exit
	else
		echo "安装hashlib成功"
		cd ../../bin
	fi
fi
	


chmod a+x *.py  2>/dev/null
chmod a+x *.sh  2>/dev/null
yes|cp -fr ../* ~/cheung/ 2>/dev/null
echo 'PATH=$PATH:~/cheung/bin' >>/etc/profile
. /etc/profile
echo "恭喜，您已经安装好了环境，接下来请您使用 ./cheungssh.py 启动程序,然后在提示符中输入操作系统命令比如： whoami "
touch ~/cheung/flag/installed
read -p  "请问是否需要安装web版本?(yes/no) " install_web
if [ -z $install_web ]
then
	echo "退出"
	exit 0
else
	if [ ${install_web} != "yes" ]
	then
		echo "退出安装程序"
		exit 0
	fi
fi
        if [ ! -d ~/cheung/ ]
        then
                yes|cp -fr ../ ~/ 2>/dev/null
                yes|cp -fr ../conf /tmp/  2>/dev/null
                if [ $? -ne 0 ]
                then
                        echo "请把../../cheung目录复制到您的宿主目录下运行!"
                        exit 1
                else
                        echo "已经把当前程序包复制到~/下面"
                fi
        else
                yes|rm -fr /tmp/conf 2>/dev/null
                yes|cp -fr  ~/cheung/conf /tmp/ 2>/dev/null
        fi

cd ~/cheung/bin
if [ $? -ne 0 ]
then
        echo  -e "无法cd 到~/cheung/bin下面\n请确保您把cheung目录复制到您了的宿主目录下面!"
        exit 1
fi


if [ ! -f ~/cheung/bin/websocket_server_cheung.py  ]
then
        echo "您的~/cheung/bin目录没有CheungSSH web启动程序!"
        exit 1
fi
which httpd 2>/dev/null
ip=`ifconfig |grep -v 'inet6'|grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' -o|grep -vE '^(127|255)|255$'|head -1`
if [ -z $ip ]
then
	read -p "抱歉，无法获取您的本机IP地址，请您手动输入您的服务器IP地址 " ip
	if [ -z $ip ]
	then
		echo "抱歉，您没有输入IP，退出安装,安装失败"
	fi
fi
		read  -p  "现在需要把web目录复制到您的http服务所在路径下，请输入您的http服务根(/)路径所在位置 (默认是/var/www/html/): " path
		if  [ -z $path ]
		then
			path="/var/www/html"
			if [ ! -d $path ]
			then
				echo "您的系统不存在$path目录,可能是因为您没有安装Apahce的原因导致的"
				exit 1
			else
				yes|cp -fr ~/cheung/web/cheungssh $path
                                if [ $? -ne 0 ]
                                then
                                        echo "复制失败"
					exit 1
                                else
                                        echo "复制成功"
                                fi
			fi
		else
			if [ ! -d $path ]
			then
				echo "您的指定的目录不存在"
				exit 1
			else
				yes|cp -fr  ../web/cheungssh/  $path
				if [ $? -ne 0 ]
				then
					echo "复制失败"
					exit 1
				else
					echo "复制成功"
				fi
			fi
		fi
		read  -p  "现在需要把搜索程序复制到您的http服务所在路径下，请输入您的http服务根(/)路径所在位置 (默认是/var/www/cgi-bin/): " cgi_path
		 if  [ -z $cgi_path ]
		then
			cgi_path="/var/www/cgi-bin/"
		fi
		chmod a+x ../web/cheungssh/*.cgi
		if [ ! -d $cgi_path ]
		then
			echo -e "您的系统不存在$cgi_path目录,可能是因为您没有安装Apahce的原因导致的\n请确保目录存在后重新安装"
			exit 1
		else
			yes|cp -fr ../web/cheungssh/*.cgi $cgi_path
			if [ $? -ne 0 ]
			then
				echo "复制失败";exit 1
			else
				echo "复制cgi成功"
			fi
		fi
#fi	


yes|cp -fr /tmp/conf ~/cheung/ 2>/dev/null

sed -i "s#ws:.*1337#ws://$ip:1337#g" ${path}/cheungssh/index.html
sed -i "s#http://.*/cgi-bin#/cgi-bin#g" ${path}/cheungssh/index.html
if  [ $? -ne 0 ]
then
	echo "初始化IP失败， 请把您的$path/cheung/index.html中的IP地址修改成您的当前主机ip"
	exit 1
fi
echo "安装完成!"
echo "正在测试程序..."
python ~/cheung/bin/cheungssh_web.py "id -u" "all"
if [ $? -ne 0 ]
then
	echo "首次安装，您的系统可能还没有配置，请您检查配置文件(~/cheung/conf/hosts)"
	read -p "按下Enter进入配置文件..." t
	vi ~/cheung/conf/hosts
	netstat -anlut|grep LISTEN|grep '0.0.0.0:1337' >/dev/null
	if [ $? -eq 0 ]
	then
		echo "系统早已启动"
		exit 1
	fi
	echo "正在启动web系统[命令 ~/cheung/bin/web_server.sh start]"
	sh ~/cheung/bin/web_server.sh start
	if  [ $? -ne 0 ]
	then
		echo "无法启动，请检查配置!"
		exit 1
	fi
	exit 1
fi
ps -fel|grep websocket_server_cheung.py|awk '{print $4}'|xargs -i kill  -9 {} 2>/dev/null
netstat -anlut|grep LISTEN|grep '0.0.0.0:1337' >/dev/null
if [ $? -eq 0 ]
then
	echo -e "系统存在残余进程，请手动清除!\n清除后可手动执行 sh ~/cheung/bin/web_server.sh 启动"
	exit 1
fi
nohup python websocket_server_cheung.py >>~/cheung/logs/web_run.log  2>&1 &
	wget -t 1  -T 2 "http://$ip/cheungssh/index.html" 2>/dev/null >/dev/null
	if  [ $? -ne 0 ]
	then
		echo -e "已经安装成功，但是似乎无法访问 http://$ip/cheungssh/index.html\n请确保您的服务器已经开起了HTTP服务"
	else
		echo  -e "已经启动Cheung Web系统请,打开浏览器访问:\n\thttp://$ip/cheungssh/index.html"
	fi
