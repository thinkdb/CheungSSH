import time,os
def test():
	i=0
	while i<10:
		os.system('echo 1 >> /tmp/a.log')
		time.sleep(1)
		i+=1

