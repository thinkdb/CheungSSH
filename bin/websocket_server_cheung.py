#!/usr/bin/python
#coding:utf8
VERSION=130
import os
HOME=os.path.expanduser("~")

os.sys.path.insert(0,"%s/cheung/bin"%HOME)
import struct,socket,os,getpass,json,cheungssh_web,split_char_size
import hashlib,commands
import threading,random
import time,re
import struct
from base64 import b64encode, b64decode
import sys
reload(sys)
sys.setdefaultencoding('utf8')
socket.setdefaulttimeout(10900000000000)
connectionlist = {}
g_code_length = 0
g_header_length = 0


def hex2dec(string_num):
    return str(int(string_num.upper(), 16))




def get_datalength(msg):
    global g_code_length
    global g_header_length    
    
    #print (len(msg))
    g_code_length = ord(msg[1]) & 127
    received_length = 0;
    if g_code_length == 126:
        #g_code_length = msg[2:4]
        #g_code_length = (ord(msg[2])<<8) + (ord(msg[3]))
        g_code_length = struct.unpack('>H', str(msg[2:4]))[0]
        g_header_length = 8
    elif g_code_length == 127:
        #g_code_length = msg[2:10]
        g_code_length = struct.unpack('>Q', str(msg[2:10]))[0]
        g_header_length = 14
    else:
        g_header_length = 6
    g_code_length = int(g_code_length)
    return g_code_length
        
def parse_data(msg,ie_key):
    global g_code_length
    g_code_length = ord(msg[1]) & 127
    received_length = 0;
    if g_code_length == 126:
        g_code_length = struct.unpack('>H', str(msg[2:4]))[0]
        masks = msg[4:8]
        data = msg[8:]
    elif g_code_length == 127:
        g_code_length = struct.unpack('>Q', str(msg[2:10]))[0]
        masks = msg[10:14]
        data = msg[14:]
    else:
        masks = msg[2:6]
        data = msg[6:]


    i = 0
    raw_str = ''


    for d in data:
        raw_str += chr(ord(d) ^ ord(masks[i%4]))
        i += 1

    if  '\x03\xe9' in raw_str.split():sys.exit()
    print "输入[%s]"%raw_str
    try:
	raw_str_source=eval(raw_str)
	raw_str=raw_str_source["cmd"]
	selectserver=raw_str_source["selectserver"]
	#print "主机: ",selectserver

    except Exception,e:
	print "命令格式错误",e
	sys.exit(1)
	
    print "已经不再接收浏览器的输入"
    return False


def sendMessage(message):
    global message_tmp
    #test
    if len(message)==0:sys.exit()
    try:
	message_tmp=eval(message.strip('\r\n'))
    except Exception,e:
	print "解析错误",e
	sys.exit(1)
    ie_key=str(message_tmp.keys()[0])
    message=str(message_tmp.values()[0])
    try:
	message_t=eval(message)
	message_t=json.dumps(message_t,encoding="UTF-8", ensure_ascii=False)#,88888888888888
	message=str(message_t)
    except Exception,e:
	pass
    #global connectionlist
    message_utf_8 = message.encode('utf-8')
    send_status='OK'
    for connection in connectionlist.keys():
        back_str = []
        back_str.append('\x81')
        data_length = len(message_utf_8)
        if data_length <= 125:
            back_str.append(chr(data_length))
	elif data_length<=65535:
		back_str.append(struct.pack('b', 126))
		back_str.append(struct.pack('>h', data_length))
        elif data_length <= (2**64-1):
            back_str.append(struct.pack('b', 127))
            back_str.append(struct.pack('>q', data_length))
        else :
                print (u'太长了')        
        msg = ''
        for c in back_str:
            msg += c;
        back_str = str(msg)   + message_utf_8#.encode('utf-8')
        if back_str != None and len(back_str) > 0:
            try:
		if connection==ie_key:
			if not message=='Done':
				source_message_dict=eval(message)
				source_message_dict_tmp=source_message_dict
				source_message_dict_tmp_warn=source_message_dict_tmp
				info=source_message_dict["content"][0]["servers"][0]["info"]
				if source_message_dict.has_key('id'):
					try:
						if is_warning:
							pass
					except:
						is_warning=False
						
					if len(message)>10000 and not is_warning:
						is_warning=True
						warning_info="""<script type="text/javascript">alert("您要看的信息太过长了!")</script>"""
						connectionlist[connection].send("\x81"+chr(len(warning_info))+warning_info)
					info_split_tmp=split_char_size.split_char_size(info)
					info_length=len(info_split_tmp)
					i=1
					for b in info_split_tmp:
						time.sleep(1)
						try:
							send_string="\x81"
							if not type({})==type(source_message_dict_tmp):
								source_message_dict_tmp=eval(source_message_dict_tmp)
							source_message_dict_tmp["content"][0]["servers"][0]["info"]=b
							if i==info_length:
								#source_message_dict_tmp["id"]=source_message_dict["id"]+"Done"
								source_message_dict_tmp["id"]=source_message_dict["id"]
						except Exception,e:
							print "转换错了",e
						source_message_dict_tmp=str(json.dumps(source_message_dict_tmp,encoding='utf-8'))
						t_data_length=len(str(source_message_dict_tmp))
						if t_data_length<126:
							send_string+=chr(t_data_length)+str(source_message_dict_tmp)
						else:
							send_string+=struct.pack('b', 126)
							send_string+=struct.pack('>h', t_data_length)
							send_string+=str(source_message_dict_tmp)
						print send_string
       			    			connectionlist[connection].send(send_string)
						i+=1
				else:
       			    		connectionlist[connection].send(back_str)
				break
			else:
				pass
				#connectionlist[connection].send('\x81'+chr(len('Done'))+'Done')
		elif ie_key=="all":
           		connectionlist[connection].send(back_str)
		else:
			continue
			print "浏览器超时了"
			connectionlist[connection].send('\x81'+chr(len('数据量太大了'))+'Done')
			connectionlist[connection].send('\x81'+chr(len('Done'))+'Done')
            except Exception,e:
		send_status='Error'
		print  "浏览器关闭连接",e
    return send_status


def deleteconnection(item):
    global connectionlist
    del connectionlist['connection'+item]


class WebSocket(threading.Thread):#继承Thread
    global dir

    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


    def __init__(self,conn,index,name,remote, path="/",ie_key="all"):
        threading.Thread.__init__(self)#初始化父类Thread
        self.conn = conn
	self.ie_key=ie_key
        self.index = index
        self.name = name
        self.remote = remote
        self.path = path
        self.buffer = ""
        self.buffer_utf8 = ""
        self.length_buffer = 0
    def run(self):#重载Thread的run
        #print('Socket%s Start!' % self.index)
        headers = {}
        self.handshaken = False

        while True:
            if self.handshaken == False:
                #print ('Socket%s Start Handshaken with %s!' % (self.index,self.remote))
		if self.remote[0]=="127.0.0.1":
			while True:
				self.conn.settimeout(1200)
				info_tmp=bytes.decode(self.conn.recv(1024))
               	 		self.buffer += info_tmp
				if not info_tmp:
					break
		else:
			self.buffer=bytes.decode(self.conn.recv(104857600))
                info=self.buffer


                if self.buffer.find('\r\n\r\n') != -1:
                    header, data = self.buffer.split('\r\n\r\n', 1)
                    for line in header.split("\r\n")[1:]:
                        key, value = line.split(": ", 1)
                        headers[key] = value


                    headers["Location"] = ("ws://%s%s" %(headers["Host"], self.path))
                    #print headers
                    key = headers['Sec-WebSocket-Key']
                    token = b64encode(hashlib.sha1(str.encode(str(key + self.GUID))).digest())


                    handshake="HTTP/1.1 101 Switching Protocols\r\n"\
                        "Upgrade: websocket\r\n"\
                        "Connection: Upgrade\r\n"\
                        "Sec-WebSocket-Accept: "+bytes.decode(token)+"\r\n"\
                        "WebSocket-Origin: "+str(headers["Origin"])+"\r\n"\
                        "WebSocket-Location: "+str(headers["Location"])+"\r\n\r\n"


                    self.conn.send(str.encode(str(handshake)))
                    self.handshaken = True  
                    #print ('Socket %s Handshaken with %s success!' %(self.index, self.remote))  
                    #sendMessage(u'Welcome, ' + self.name + ' !')  #像浏览器发送消息
                    #sendMessage(unicode("欢迎使用CheungSSH Web版本! QQ:2418731289").encode('utf-8'))  #像浏览器发送消息
                    #os.system("python %s/cheung/bin/get_info.py"%HOME)
                    #print first_info,555555555555
                    #sendMessage(unicode("""<script type="text/javascript">alert("欢迎使用CheungSSH Web版本! QQ:2418731289")</script>""").encode('utf-8'))  #像浏览器发送消息
                    i=1
                    #print self.buffer_utf8
                    sendMessage("""{"%s":{"content": [{"servers": [{"info": "%s"}]}], "msgtype": "token", "id": "%s"}}"""  % (self.ie_key,self.ie_key,self.ie_key))  #像浏览器发送消息
                    self.buffer_utf8 = ""
                    g_code_length = 0                    
		else:
			#info=json.dumps(info,encoding='utf8',ensure_ascii=False)
			#info=str(info)
			T=sendMessage(info)
			if T=='Error':
				print "断开接收通道"
				deleteconnection(str(self.index))
				break
				


            else:
                global g_header_length
		mm=''
		try:
			while True:
				self.conn.settimeout(0.5)
				mm+=self.conn.recv(1024)
		except Exception:
			pass
                if len(mm) <= 0:
                    continue
                if g_code_length == 0:
                    get_datalength(mm)
                #接受的长度
                self.length_buffer = self.length_buffer + len(mm)
                self.buffer = self.buffer + mm
                if self.length_buffer - g_header_length < g_code_length :
                    continue
                else :
                    self.buffer_utf8 = parse_data(self.buffer,self.ie_key) #utf8                
                    msg_unicode = str(self.buffer_utf8).decode('utf-8', 'ignore') #unicode
                    if msg_unicode=='quit':
                        #print (u'Socket%s Logout!' % (self.index))
                        nowTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
                        #sendMessage(u'%s %s say: %s' % (nowTime, self.remote, self.name+' Logout'))                      
                        #sendMessage(u'AAA')                 
                        #deleteconnection(str(self.index))
                        self.conn.close()
                        break #退出线程
                    else:
                        #print (u'Socket%s Got msg:%s from %s!' % (self.index, msg_unicode, self.remote))
                        nowTime = time.strftime(u'%H:%M:%S',time.localtime(time.time()))
                        #sendMessage(u'%s %s say: %s' % (nowTime, self.remote, msg_unicode))  
                        #sendMessage(u'Starting')                 
                    #重置buffer和bufferlength
                    self.buffer_utf8 = ""
                    self.buffer = ""
                    g_code_length = 0
                    self.length_buffer = 0
            self.buffer = ""


class WebSocketServer(object):
    def __init__(self):
        self.socket = None
    def begin(self):
        print( 'WebSocketServer Start!')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.bind(("0.0.0.0",1337))
        self.socket.listen(50)


        global connectionlist


        while True:
            i=str(random.randint(90000000000000000000,99999999999999999999))
            connection, address = self.socket.accept()
            print '客户端ip',address
            username=address[0]     
            ie_key='connection'+i
            path="/"
            newSocket = WebSocket(connection,i,username,address,path,ie_key)
            newSocket.start() #开始线程,执行run函数
            connectionlist[ie_key]=connection


if __name__ == "__main__":
    server = WebSocketServer()
    server.begin()
