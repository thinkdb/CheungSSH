#!/usr/bin/python
#coding:utf8
import os,cgi,sys,json,commands,re,urllib
#query_string:cmd=ifconfig&path=/tmp
def get_query_string():
	result=[]
	head_string=""
	try:
		source_string=urllib.unquote(os.environ['QUERY_STRING'])
		add_string='&'.join(source_string.split('&')[:-2])
		#print "<pre>"+source_string+']</pre>'
		try:
			callback="&".join(source_string.split('&')[-2:]).split('=')
			callback_key=callback[0]
			if callback_key!="callback":
				return "Unkown request Format!</br>Format: path_search.cgi?ifcon&callback=abc&123</br><h1> CheungSSH web system</h1>"
			callback_value=callback[1].split('&')[0]
		except Exception,e:
			#return "Parse Error",e
			return []
		i=0
		all_string=add_string.split()
		search_value=all_string[0]
			
		isTmpend=False
		if len(all_string)==1:
			local_path_tmp=local_path(search_value)
			local_cmd_tmp=local_commands(search_value)
			result=local_path_tmp+local_cmd_tmp
		else:
			#head_string=" ".join(all_string[:-1])
			search_value=all_string[-1]
			head_string=add_string.split(search_value)[0]
			head_string=search_value.join(add_string.split(search_value)[:-1])#  "/va".join(a.split('/va')[:-1])
			local_path_tmp=local_path(search_value)
			result=result+local_path_tmp
		if re.search(" +$",add_string):
			isTmpend=True
			#head_string=" ".join(all_string[:-1])
			head_string=add_string
			search_value="/"
			local_path_tmp=local_path(search_value)
			result=result+local_path_tmp
			
	except Exception,e:
		#return "Err",e
		return []
	result=sorted(list(set(result)))
	#result=str(json.dumps(result,encoding='utf8',ensure_ascii=False))
	new_result=[]
	for a in result:
		if isTmpend:
			new_result.append(add_string+a)
			#print "<pre>["+all_string+"]</pre>"
			#print all_string
		elif len(all_string)==1:
			new_result.append(head_string+a)
		else:
			#new_result.append(head_string +" "+a)
			new_result.append(head_string +a)
	new_result=str(json.dumps(new_result,encoding='utf8',ensure_ascii=False))
	return callback_value+"("+new_result+")"

def local_commands(cmd=""):
    a=commands.getoutput("PATH=$PATH:./:/usr/lib:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/cheung/bin;for c in $(echo $PATH |sed 's/:/ /g');do ls $c;done").strip().split('\n')
    result_cmd=[]
    for b in a:
        c=re.search("^%s.*"%(cmd),b)
        if c:
                result_cmd.append(c.group())
        else:
                continue
    return result_cmd
def local_path(path='/'):
        result1=[]
        result=[]
        try:
                root_path=os.path.dirname(path)
                son_path=os.path.basename(path)
                if os.path.exists(root_path):
                        result1=commands.getoutput('''find %s  -maxdepth 1 -name "%s*"'''%(root_path,son_path)).split('\n')
                else:
                        pass
        except Exception,e:
                print "[111]"
                pass
        try:
                for f in os.listdir(path):
                        qf = os.path.join(path,f)
                        if os.path.isdir(qf):
                                result.append(f+os.sep)
                        else:
                                result.append(f)
        except Exception,e:
                pass
        result_all=result+result1
	new_result_all=[]
	for a in result_all:
		all_path=os.path.join(path,a)
		if os.path.exists(all_path):new_result_all.append(all_path)
	return new_result_all

















	
print "Content-type: text/html\n"
print get_query_string()
