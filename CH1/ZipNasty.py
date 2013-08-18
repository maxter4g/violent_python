'''
Created on Mar 20, 2013
modified by maxter 
funzione in python 2 .7(non tollera le lettere spagnole) e 3.2(piu veloce) 


to do list

1 capire se il path puo' essere relativo
2 come bloccare quando trova la password (ok)
3 contatore (inserita progressbar ma funziona solo in 2.6 e non in thread )
4 eliminare la b nel print out

@author: NNRooth
'''
# from progressbar import ProgressBar
import zipfile
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
        exit.__init__(main)
        flg = 1
        exit()
#        if Thread.is_alive():
#            try:
#                 Thread._Thread__stop()
#                 Thread.quit
#            except:
#                 print(str(Thread.getName()) + ' could not be terminated')        
                
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
     #   i = 0

        s = line.strip()
 #       stdout.write('\t%s\r' % s)
 #       stdout.write("Download progress: %d%%   \r" % (i) )
 #       stdout.flush()
        i = i+1
 #       stdout.write(":".join("{0:x}".format(ord(c)) for c in s))
        stdout.write('\t%s\n' % password)
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
##    stdout.write('[+] Zip Nasty!!!\n')
    
##    zipfilename = input('[.] Zip File Path: ')
##    dicfilename = input('[.] Dic File Path: ')
    zipfilename = '/root/Desktop/ViolentPython/CH1/zipTest/secrets.zip'
#  dicfilename = '../dictionary.txt'   
    dicfilename = '/root/Desktop/ViolentPython/CH1/zipTest/dictionaryBig2.txt'   
    if not (zipfile.is_zipfile(zipfilename)):
        stdout.write('[-] %s is not a zip file...\n' % zipfilename)
        exit(0)
    else:
        stdout.write('[*] Decrypting %s  .. please wait....\n' % zipfilename)
 #       stdout.write('[*] Please wait...')
    
    decryptZip(zipfilename, dicfilename)
##    stdout.write('[!] Done\n')

if __name__ == '__main__':
    main()
