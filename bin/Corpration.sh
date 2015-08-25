#!/bin/bash
stty intr undef
stty -echo
clear
Corp="Corpright 2013-2015 Cheung Kei-Chuen All Rights Reserved"
info(){
	printf "\033[?25l"
	i=0
	while [ $i -le 96 ]
		do
		printf "_"
		sleep 0.02
		let i++
	done
	echo -e "\n"
}
show(){
	#printf "\033[12;96H"
	printf "\033[0;98H"
	i=0
	while [ $i -le 5 ]
	do
      		 printf "\b/"
	        sleep 0.05
	        printf "\b-"
	        sleep 0.05
 	       printf "\b\\"
	        sleep 0.05
	        printf "\b|"
	        sleep 0.05
		let i++
	done
	printf "\b "
	printf "\033[?25h"
}
info
show
printf "\033[?25l"
echo -en "\t";
corpration(){
		echo -e "\n\t\t\t"
		echo "Welcome to use CheungSSH Linux/Unix Automation Tools!"|awk  'END{a=length($0);i=1;printf "\n\n\t\t";while(i<=a){printf substr($0,i,1) "\a";i++;system("sleep  0.1")} ;"printf \n"}'
		echo "Author: Cheung Kei-Chuen"|awk  'END{a=length($0);i=1;printf "\n\n\t\t";while(i<=a){printf substr($0,i,1) "\a";i++;system("sleep  0.1")} ;"printf \n"}'
		echo "Jobs: China Mobile Internet Automation Deployment"|awk  'END{a=length($0);i=1;printf "\n\n\t\t";while(i<=a){printf substr($0,i,1) "\a";i++;system("sleep  0.1")} ;"printf \n"}'
		echo "$Corp"|awk  'END{a=length($0);i=1;printf "\n\n\t\t";while(i<=a){printf substr($0,i,1) "\a";i++;system("sleep  0.1")} ;"printf \n"}'
		echo "QQ: 2418731289"|awk  'END{a=length($0);i=1;printf "\n\n\t\t";while(i<=a){printf substr($0,i,1) "\a";i++;system("sleep  0.1")};printf "\n" }'
		echo "Download: http://blog.chinaunix.net/uid-29295703-id-4663051.html"|awk  'END{a=length($0);i=1;printf "\n\n\t\t";while(i<=a){printf substr($0,i,1) "\a";i++;system("sleep  0.1")};printf "\n" }'
}
endline1(){
	i=0
	printf "\033[0;98H"
	while [ $i -le 105 ]
	do
       	 	printf "+_"
	        #printf "\033[2D"
	        printf "\033[3D"
	        let i++
	        sleep 0.03
	done
	printf "__"
}
endline1
corpration
printf "\n\033[?25h\n"
stty intr ^c
stty echo
