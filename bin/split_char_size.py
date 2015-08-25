import json
#coding:utf-8
def split_char_size(char):
	char=char.decode('utf-8')
	nowchar=''
	char_list=[]
	while char:
		if len(char)>=10000:
			nowchar=char[:10000]
			char = char[10000:]
		else:
			nowchar = char
			char=''
		#char_list.append(json.dumps(nowchar,encoding='utf8',ensure_ascii=False))
		char_list.append(nowchar)
	return char_list
