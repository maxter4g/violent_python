"""
to do list

 verify python 3

"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from sys import stdout
# import optparse
from socket import *

#import socket
from threading import *
#from socket import socket
screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):

##    HOST = 'daring.cwi.nl'                 # Symbolic name meaning all available interfaces
##    PORT = 80            # Arbitrary non-privileged port
##    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##    s.connect(('213.205.32.10', PORT))
##    s.listen(1)
##    conn, addr = s.accept()
##    print('Connected by', addr)



    try:
##        host = '192.168.1.3'                 # Symbolic name meaning all available interfaces
##        port = 5900            # Arbitrary non-privileged port
##        host = '213.205.32.10'                 # Symbolic name meaning all available interfaces
##        port = 80            # Arbitrary non-privileged port

##        connskt = socket()
##        connskt.connect((host,port))
##        banner = connskt.recv(128).decode('utf-8', 'ignore').strip('\n').strip('\r')


##        tgtHost = '192.168.1.3'
##        tgtPort = 5900
##
##        tgtHost = '213.205.32.10'
##        tgtPort = 80
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'Hello, world')
  #      connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        stdout.write('\n')
        stdout.write('[+] tcp open %s' % tgtPort + '\n')
#        print '[+] %d/tcp open' % tgtPort
#        stdout.write('\n')
        if verbose_Flg == "Y":
            stdout.write('[+] '+ str(results)+ '\n')
            stdout.write('\n')
#        print '[+] ' + str(results)
    except Exception as e:
        if verbose_Flg == "Y":
            print(e)
        screenLock.acquire()
#        stdout.write('\n')
        stdout.write('[-] tcp closed %s' % tgtPort + '\n')
#        print '[-] %d/tcp closed' % tgtPort
    finally:
    	screenLock.release()
    connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
##        pass
        tgtIP = gethostbyname(tgtHost)

    except Exception as e:
        if verbose_Flg == "Y":
            print(e)
        stdout.write('[-] Cannot resolve %s: Unknown host' % tgtHost + '\n')
#        print "[-] Cannot resolve '%s': Unknown host" %tgtHost
        return

    try:
        tgtName = gethostbyaddr(tgtIP)

        stdout.write('[+] Scan Results for: %s ' % tgtName[0] + '%s' % tgtName[2]+ ' on port(s): %s ' % tgtPorts + '\n')
        stdout.write('[+] please wait...' + '\n')
#        print '\n[+] Scan Results for: ' + tgtName[0]
    except:
        pass
#        print '\n[+] Scan Results for: ' + tgtIP
 #       stdout.write('[+] Scan Results for: %s' % tgtIP + '\n')
  #  socket.setdefaulttimeout(1)

    for tgtPort in tgtPorts:
            if Thread_Flg == "N":
                connScan(tgtHost,int(tgtPort))
            else:
                t = Thread(target=connScan,args=(tgtHost,int(tgtPort)))
                t.start()

def main():

    global Thread_Flg
    global verbose_Flg

    ver = sys.version.split(' ')[0]

    if ver[0] == "3":
        ans = input('[.] Host: ')
    else:
        ans = raw_input('[.] Host: ')

    if ans == "":
        tgtHost = 'www.tiscali.it'
    else:
        tgtHost = ans

    if ver[0] == "3":
    	ans = input('[.] Port - separated by comma: ')
    else:
        ans = raw_input('[.] Port - separated by comma: ')
    if ans == "":
        tgtPort = '80,53,23,101,5900'
    else:
        tgtPort = ans

    if ver[0] == "3":
    	ans = input('[.] Verbose - default No: ')
    else:
        ans = raw_input('[.] Verbose - default No: ')
    if ans == "":
        verbose_Flg = 'N'
    else:
        verbose_Flg = "Y"

    if ver[0] == "3":
    	ans = input('[.] Thread - default No: ')
    else:
        ans = raw_input('[.] Thread - default No: ')
    if ans == "":
        Thread_Flg = 'N'
    else:
        Thread_Flg = "Y"
    tgtPorts = str(tgtPort).split(',')
    portScan(tgtHost, tgtPorts)
    stdout.write('[!] Done\n')

if __name__ == '__main__':
    main()
