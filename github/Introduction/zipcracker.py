import sys

import crypt
import zipfile 

from threading import Thread

def extractFile(file,password):
    try:
        file.extractall(pwd=password)
        print( '[+] The password is: '+password )
        sys.exit()
    except:
        pass
    return

def main():
    if len(sys.argv) != 2:
        print( 'invalid number of arguments')
        exit(0)    
    zfile = zipfile.ZipFile(sys.argv[1])
 #   zfile = 'secrets.zip'
    dict = open('/root/Desktop/Introduction/dictionary.txt','r')
    for word in dict.readlines():
        word = word.strip('\n') 
        thread = Thread(target=extractFile,args=(zfile,word))
        thread.start() 
    print( '[-] Password not found.') 


if __name__ == "__main__":
    main()
