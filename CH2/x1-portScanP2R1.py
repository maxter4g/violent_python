"""
to do list

 doesn't work in python3

"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from sys import stdout
# import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        stdout.write('\n')
        stdout.write('[+] tcp open %s' % tgtPort + '\n')
#        print '[+] %d/tcp open' % tgtPort
#        stdout.write('\n')
        stdout.write('[+] '+ str(results)+ '\n')
        stdout.write('\n')
#        print '[+] ' + str(results)
    except:
        screenLock.acquire()
#        stdout.write('\n')
        stdout.write('[-] tcp closed %s' % tgtPort + '\n')
#        print '[-] %d/tcp closed' % tgtPort
    finally:
    	screenLock.release()
    connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        stdout.write('[-] Cannot resolve %s: Unknown host' % tgtHost + '\n')
#        print "[-] Cannot resolve '%s': Unknown host" %tgtHost
        return

    try:
        tgtName = gethostbyaddr(tgtIP)

        stdout.write('[+] Scan Results for: %s ' % tgtName[0] + '%s' % tgtName[2]+'\n')
#        stdout.write('[+] %d/Scan Results for: %s' % tgtName + '\n')
#        print '\n[+] Scan Results for: ' + tgtName[0]
    except:
#        print '\n[+] Scan Results for: ' + tgtIP
        stdout.write('[+] Scan Results for: %s' % tgtIP + '\n')
    setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        if Thread_Flg == "N":
            connScan(tgtHost,int(tgtPort))
        else:
            t = Thread(target=connScan,args=(tgtHost,int(tgtPort)))
            t.start()

def main():

    global Thread_Flg

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
        tgtPort = '80,53,23,101'
    else:
        tgtPort = ans

    if ver[0] == "3":
    	ans = input('[.] Thread - default N: ')
    else:
        ans = raw_input('[.] Thread - default N: ')
    if ans == "":
        Thread_Flg = 'N'
    else:
        Thread_Flg = "Y"



#    parser = optparse.OptionParser('usage %prog '+\
#      '-H <target host> -p <target port>')
#    parser.add_option('-H', dest='tgtHost', type='string',\
#      help='specify target host')
#    parser.add_option('-p', dest='tgtPort', type='string',\
#      help='specify target port[s] separated by comma')

#    (options, args) = parser.parse_args()

#    tgtHost = options.tgtHost
#    tgtPorts = str(options.tgtPort).split(',')

#    if (tgtHost == None) | (tgtPorts[0] == None):
#	print parser.usage
#        exit(0)
    tgtPorts = str(tgtPort).split(',')


    portScan(tgtHost, tgtPorts)

    stdout.write('[!] Done\n')


if __name__ == '__main__':
    main()