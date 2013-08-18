import sys

import crypt
import zipfile 

from threading import Thread

def extractFile(file,password):
    try:
#        print('testing pwd = '+password)
        file.extractall(pwd=password)
        print( '[+] The password is: '+password )
        sys.exit('fine')
    #    quit()
    #    raise SystemExit
    except:
        pass
    return

def main():
    if len(sys.argv) != 2:
        print( 'invalid number of arguments')
        exit(0) 
    # sys.argv[1]='/root/Desktop/ViolentPython/CH1/secrets.zip'
    zfile = zipfile.ZipFile(sys.argv[1])
    # zfile = '/root/Desktop/ViolentPython/CH1/secrets.zip'
    dict = open('/root/Desktop/ViolentPython/CH1/dictionaryBig.txt','r')
    for word in dict.readlines():
        word = word.strip('\n') 
#        extractFile(zfile,word)
        thread = Thread(target=extractFile,args=(zfile,word))
        thread.start() 
    print( '[-] Password not found.') 


if __name__ == "__main__":
    main()
