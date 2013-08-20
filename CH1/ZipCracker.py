'''
Created on Mar 20, 2013 by NNRooth
Thanks to  NNRooth at https://github.com/nnrooth/Violent-Python-33/tree/master/Violent Python 33

modified by maxter4g

Rev 1

works in python 2 .7 e 3.2(faster) 

to do list
1-progessbar do not work inside thread



'''
# from progressbar import ProgressBar
import zipfile
import sys
import os
from sys import stdout
from threading import Thread
from threading import Semaphore

threadLock = Semaphore(value=1)

def extractZip(zipFile, password):
    flg = 0
    try:
        zipFile.extractall(pwd=password)
        stdout.write('\n')
        stdout.write('[+] Password Found: %s' % password.decode() + '\n')
        stdout.write('\n')
        stdout.write('[!] Successfully Done\n')
        exit.__init__(main)
        flg = 1
        exit()         
        Thread._stop()
    except:
        if flg == 1:
            exit.__init__(main)
 #           Thread._stop()
            exit()
            exit[(0)]
        pass

def decryptZip(zipfilename, dicfilename):
    zFile = zipfile.ZipFile(zipfilename)
    pFile = open(dicfilename)
    
    maxThreads = 30
    threadCount = 0
    i = 0
    for line in pFile.readlines():
        password = line.strip().encode('utf-8', 'strict')

        s = line.strip()
 #       stdout.write('\t%s\r' % s)
 #       stdout.write("Download progress: %d%%   \r" % (i) )
 #       stdout.flush()
        i = i+1
 #       stdout.write(":".join("{0:x}".format(ord(c)) for c in s))
        stdout.write('\t%s\n' % s)
        t = Thread(target=extractZip, args=(zFile, password))
        
 #       pbar = ProgressBar(10)
 #       for c in range(10):
 #           pbar.update(c+1)
                       
        threadCount += 1
        if (threadCount >= maxThreads):
            threadCount = 0
            t.start()
        extractZip(zFile, password)
    t.start()
        
    return None

def main():
    ver = sys.version.split(' ')[0]

    zipfilename = '/root/Desktop/ViolentPython/CH1/zipTest/secrets.zip'
    
    if ver[0] == "3":
        ans = input('[.] Zip File Path: ')
    else:	
        ans = raw_input('[.] Zip File Path: ')
    
    if ans == "":
        zipfilename = '/root/Desktop/ViolentPython/CH1/zipTest/secrets.zip'
    else:
        zipfilename= ans
        
    if ver[0] == "3":
    	ans = input('[.] Dic File Path: ')
    else:
        ans = raw_input('[.] Dic File Path: ')
    if ans == "":
        dicfilename = '/root/Desktop/ViolentPython/CH1/zipTest/dictionaryBig2.txt' 
    else:
        dicfilename= ans
        
        if os.path.exists(dicfilename):
            pass
        else:
            stdout.write('\n')
            stdout.write('[-] %s not found...\n' % dicfilename)   
            exit(0) 
    if not (zipfile.is_zipfile(zipfilename)):
        stdout.write('[-] %s not found...\n' % zipfilename)
        exit(0)
    else:
        stdout.write('[*] Decrypting %s  .. please wait....\n' % zipfilename)
    
    decryptZip(zipfilename, dicfilename)
    stdout.write('[!] Unsuccessfully Done\n')

if __name__ == '__main__':
    main()
