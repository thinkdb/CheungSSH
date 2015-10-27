#/usr/bin/python
#coding:utf8
import os,sys,paramiko
def UploadFile(sdir,ddir,username,password,ip,loginmethod,port=22,force=False):
	if not ddir.endswith('/'):
		ddir=ddir+"/"
	if not sdir.endswith('/'):
		sdir=sdir+"/"
	if not os.path.isdir(sdir):
		return False,"Local Directory not exists"
	try:
		t=paramiko.Transport((ip,int(port)))
		if loginmethod=="key".upper():
			keyfile=keyfile
			key=paramiko.RSAKey.from_private_key_file(keyfile)
			t.connect(username = username,pkey=key)
		else:
			t.connect(username = username,password = password)
		sftp = paramiko.SFTPClient.from_transport(t)
		try:
			sftp.stat(ddir)
		except Exception,e:
			if e.errno==2 and not force:
				print '-ERR'
				return False,"Remote directory not  exists"
		all_dirs=[]
		all_files=[]
		remote_all_dirs=[]
		for root,dirs,files in os.walk(sdir):
			for dir in dirs:
				local_full_dir=os.path.join(root,dir)
				all_dirs.append(local_full_dir)
				local_sub_dir=local_full_dir.split(sdir)[1]
				remote_full_dir=os.path.join(ddir,local_sub_dir)
				i=1;c=remote_full_dir.split('/')[1:]
				for d in c:
					remote_and_local_dir="/"+'/'.join(c[:i])
					remote_all_dirs.append(remote_and_local_dir)
					i+=1
					try:
						sftp.stat(remote_and_local_dir)
					except Exception,e:
						if e.errno==2:
							sftp.mkdir(remote_and_local_dir)
						else:
							print '-ERR'
							return False,e
			for file in files:
				local_full_file=os.path.join(root,file)
				all_files.append(local_full_file)
				new_remote_full_file=local_full_file.replace(sdir,ddir)
				try:
					sftp.put(local_full_file,new_remote_full_file)
				except Exception,e:
					print '-ERR'
					return False,e
		remote_all_dirs=list(set(remote_all_dirs))
		#print remote_all_dirs
		#print all_dirs,"dir"
		#print all_files,"file"
		#sftp.put(sfile,dfile)
		print "+OK"
		return True,"+OK"
	except Exception,e:
		return False,e
