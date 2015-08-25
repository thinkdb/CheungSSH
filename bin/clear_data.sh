#!/bin/bash
rm -f ~/cheung/conf/hosts


find  ~/cheung/bin -type f -name '*pyc' -exec rm -f {} \;
find  ~/cheung/flag -type f  -exec rm -f {} \;
find  ~/cheung/version -type f  -exec rm -f {} \;
rm -f ~/cheung/logs/*
rm -fr ~/cheung/data/*
cat >~/cheung/conf/hosts<<EOF
[Hosts-Group1]
#主机地址===端口===登陆账户===登陆密码===su-root密码
#[Hosts-Group2]
#支持多个主机组
#如果您担心安全问题，在密码列位置，您可以使用...===None===...表示不在配置文件中指定，而是在您执行命令的时候系统会询问您密码。比如以下配置:
#127.0.0.1===22===root===None===None
#locallhost===222===root===your-root's-password===su-root的密码,如果没有使用Useroot，此列也可以填写None
#None的特殊指定只能针对密码特别指定，不能在账户名，或者是端口，主机这三列中使用
#注意:在每一个配置中，请不要有空格或者是制表符!
#在所有的配置列中，请用三个等于（===）分割开，并确保有5列！
EOF
