#!/usr/bin/python
import hashlib
import sys 

def main(filename):
    m = hashlib.md5()
    with open(filename, 'rb') as fp: 
        while True:
            blk = fp.read(4096) # 4KB per block
            if not blk: break
            m.update(blk)
    #print m.hexdigest(), filename
    return  m.hexdigest()

if __name__ == '__main__':
	try:
    		print main(sys.argv[1])
	except:
        	sys.exit('Usage: %s file' % sys.argv[0])
