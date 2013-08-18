#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import os
import sys


def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return


def stampa(banner, filename):

    f = open(filename, 'a')
    f.writelines("\n" +str(ip)+" - "+str(port)+"   "+str(banner))
    print("--------------"+str(ip)+"-"+str(port))
    f.close()

def checkVulns(banner, filename):
    return
#    for line in f.readlines():
#        if line.strip('\n') in str(banner):
#            print( '[+] Server is vulnerable: ' +\
#               banner.strip('\n'))


def main():

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print( '[-] ' + filename +\
                ' does not exist.')
            exit(0)

        if not os.access(filename, os.R_OK):
            print( '[-] ' + filename +\
                ' access denied.')
            exit(0)
    else:   
        print( '[-] Usage: ' + str(sys.argv[0]) +\
            ' <vuln filename>')
        exit(0)

    portList = [21,22,25,80,110,443]
    global ip
    global port
    for x in range(1, 250):
	    ip = '192.168.1.' + str(x)
	    print(">>>>>>"+str(ip))
	    for port in portList:
		    print(str(port))
		    banner = retBanner(ip, port)
		    stampa(banner, "result1.txt")
		    if banner:
			    print( '[+] ' + ip + ' : ' + str(port)+ " " +str(banner))
			    checkVulns(banner, filename)


if __name__ == '__main__':
    main()
