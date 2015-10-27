#!/usr/bin/python
VERSION=1.3
import os,sys,commands
def Get_Char(Char):
	New_Char=[]
	for m in Char.split('\n'):
		New_Char.append("</br>"+m.replace("<","&lt;")+'   ')
	New_Char="".join(New_Char)
	return New_Char
def Show_Char(Char,Color_Status):
	Char=Get_Char(Char)
	AllChar=''
	if Color_Status==0:
		Color_Start=""
		Color_End=""
	else:
		Color_Start="""<div style="color:red">"""
		Color_End="""</div>"""
	AllChar="<pre>"+Color_Start+Char+Color_End+"</pre>"
	#AllChar="<pre>"+Char+"</pre>"
	#print AllChar
	return AllChar

