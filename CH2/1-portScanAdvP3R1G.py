#!/usr/bin/python
# -*- coding: utf-8 -*-
## Standard Import
import sys
import os
from sys import stdout
from socket import *
#from socket import socket
#import socket
from threading import *
from threading import Semaphore
##from socket import setdefaulttimeout
##from threading import Thread
from sys import platform as _platform
import time

## No Standard Imports
try:
    import pygeoip
    geo_Flg = "Y"
except:
    geo_Flg = "N"
    stdout.write('\n[?] Module pygeoip Not found--DISABLED\n')
finally:
    pass
try:
    import nmap
    nmap_Flg = "Y"
except:
    nmap_Flg = "N"
    stdout.write('\n[?] Module nmap Not found--DISABLED\n')
finally:
    pass

screenLock = Semaphore(value=1)
scan_list = []

##thread_lock = Semaphore(value=1)
##
def getGeoLoc(host):

    __dir__ = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(__dir__, 'GeoDat/Geo.dat')
#    f = open(filepath, 'w')   
    
#    if geo_Flg != "N": gi = pygeoip.GeoIP('/root/Desktop/ViolentPython/CH2/GeoDat/Geo.dat')
    if geo_Flg != "N": gi = pygeoip.GeoIP(filepath)

    try:
        rec = gi.record_by_name(host)
        city = rec['city']
        state = rec['region_name']
        country = rec['country_name']
        longitude = rec['longitude']
        latitude = rec['latitude']

        if city != '' and state != '':
            geoLoc = '%s,%s,%s : %6f,%6f' % (city, state, country, longitude, latitude)
        elif city != '':
            geoLoc = '%s,%s : %6f,%6f' % (city, country, longitude, latitude)
        else:
            geoLoc = '%s : %6f,%6f' % (country, longitude, latitude)
    except:
        geoLoc = 'Unregistered'
    finally:
        return geoLoc


def nmapScan(tgtHost,tgtPort):

    try:
        tgtHost = gethostbyname(tgtHost)
        nmScan = nmap.PortScanner()
        nmScan.scan(tgtHost, tgtPort)
        state=nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
        if state == 'closed':
            pass
        else:
            pass
#            thread_lock.acquire()
    except:
        pass
    finally:
        pass
 #       thread_lock.release()
    scan_list.append('\n%s : %s : %s : %s' % (tgtHost, tgtPort, state, ""))
    stdout.write('[+] tcp %s %s' % (state, tgtPort) + '\n')


def saveList2Log():
    if not scan_list:
        return
    logDoc = ''
    for line in scan_list:
        logDoc += line.strip() + '\n'
    try:
# This will create a new file or **overwrite an existing file**.
# user/workspace/Python 3/file.log
        __dir__ = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(__dir__, 'file.log')
        f = open(filepath, 'w')                
#        f = open("file.log", "w")
        try:
            f.writelines(logDoc) # Write a sequence of strings to a file
        finally:
            f.close()
    except Exception as e:
        stdout.write('\n[-] Err: %s' % e)
        pass

def parsePort(ans):
    try:
        if ans == "":
            tgtPort = '80,443,22,5900,10000'
        elif ans == "D":
            tgtPort = '80,443,22,5900,10000'
        elif ans == 'S':
            tgtPort = '20,21,22,23,25,43,53,80,110,143,443,464,1080,1194,1900,4444,9988'
        elif '-' in ans:
            ports = []
            p_range = ans.split('-')
            for p in range(int(p_range[0]), int(p_range[1]) + 1):
                ports.append(p)
                tgtPort = str(ports).replace('[','')
                tgtPort = tgtPort.replace(']','')
        elif 'F' in ans:
            try:
                __dir__ = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(__dir__, 'ports.txt')
                dictFile = open(filepath, 'r')                
#                dictFile = open('/root/workspace/ports.txt', 'r')
            except Exception as e:
                 stdout.write('\n[-] Err: %s' % e)
                 exit(__main__)
            
            ports = []
            for line in dictFile.readlines():
                 ports.append(int(line.strip()))
            tgtPort = str(ports).replace('[','')
            tgtPort = tgtPort.replace(']','')
            dictFile.close()
        else:
            tgtPort = ans
        return tgtPort
    except Exception as e:
#        pass
        if verbose_Flg == "Y":
            print(e)

def parseTime(time):
    hours = time / 60 / 24
    minutes = time /60 % 60
    seconds = time % 60
    return '%d hr : %d min : %d sec' % (hours, minutes, seconds)


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'Hello, world')
        results = connSkt.recv(20)
        banner = connSkt.recv(128).decode('utf-8', 'ignore').strip('\n').strip('\r')
#        screenLock.acquire()
        scan_list.append('\n%s : %s : %s : %s' % (tgtHost, tgtPort, banner, results))
        stdout.write('\n')
        stdout.write('[+] tcp open %s' % tgtPort + '\n')
        if verbose_Flg == "Y":
            stdout.write('[+] '+ str(results)+ '\n')
            stdout.write('\n')
    except Exception as e:
        if verbose_Flg == "Y":
            print(e)
#        screenLock.acquire()
        stdout.write('[-] tcp closed %s' % tgtPort + '\n')
    finally:
 #   	screenLock.release()
           connSkt.close()


def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
        stdout.write('[+] Scan Results for: %s ' % tgtIP +'(' +'%s' % tgtHost+ ') on port(s): %s ' % tgtPorts + '\n')
        if geo_Flg != "N":
            geoLoc = getGeoLoc(tgtHost)
            stdout.write('[+] Host Location: %s ' % geoLoc +'(' +'%s' % tgtHost+ ')' + '\n')
        stdout.write('[+] please wait...til Done' + '\n')
    except Exception as e:
        if verbose_Flg == "Y":
            print(e)
        stdout.write('[-] Cannot resolve %s: Unknown host' % tgtHost + '\n')
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
#        stdout.write('[+] Scan Results for: %s ' % tgtName[0] + '%s' % tgtName[2]+ ' on port(s): %s ' % tgtPorts + '\n')
#        stdout.write('[+] please wait...' + '\n')
    except Exception as e:
        if verbose_Flg == "Y":
##            print(e)
             pass
  #  socket.setdefaulttimeout(1)
    for tgtPort in tgtPorts:
            if Thread_Flg == "N":
                if nmap_Flg == "N":
                    connScan(tgtHost,int(tgtPort))
                else:
                    nmapScan(tgtHost, tgtPort)
            else:
                
                if nmap_Flg == "N":
                    t = Thread(target=connScan,args=(tgtHost,int(tgtPort)))
                    t.start()
                else:
                    t = Thread(target=nmapScan,args=(tgtHost,tgtPort))
                    t.start()
                    
                   # nmapScan(tgtHost, tgtPort)

def main():

    global Thread_Flg
    global verbose_Flg
    global log_Flg
    global nmap_Flg
    global geo_Flg
        
    ver = sys.version.split(' ')[0]

    if ver[0] == "3":
        ans = input('[.] Host? (IP or domain): ').upper()
    else:
        ans = raw_input('[.] Host? (IP or domain): ').upper()
    if ans == "":
        tgtHost = '192.168.1.169'
    elif ans == "D":
        tgtHost = 'www.tiscali.it'
    else:
        tgtHost = ans

    ans = ""
    if ver[0] == "3":
        ans = input('Ports: [s]tandard, [ ]or[d]efault,[p1-p2]range, [f]ile : ').upper()
    else:
        ans = raw_input('Ports: [s]tandard, [ ]or[d]efault,[-]range, [f]ile : ').upper()
    tgtPort = parsePort(ans)

    if ver[0] == "3":
    	ans = input('[.] Verbose - default Yes: ').upper()
    else:
        ans = raw_input('[.] Verbose - default Yes: ').upper()
    if (ans == "" or ans == "Y"):
        verbose_Flg = 'Y'
    else:
        verbose_Flg = "N"
    if ver[0] == "3":
    	ans = input('[.] Thread - default No: ').upper()
    else:
        ans = raw_input('[.] Thread - default No: ').upper()
    if (ans == "" or ans == "N"):
        Thread_Flg = 'N'
    else:
        Thread_Flg = "Y"

    if ver[0] == "3":
    	ans = input('[.] Save log - default Yes: ').upper()
    else:
        ans = raw_input('[.] Save log - default Yes: ').upper()
    if (ans == "" or ans == "Y"):
        log_Flg = 'Y'
    else:
        log_Flg = "N"

    if nmap_Flg != "N":
        if ver[0] == "3":
            ans = input('[.] Use Nmap - default No: ').upper()
        else:
            ans = raw_input('[.] Use Nmap - default No: ').upper()
        if (ans == "" or ans == "N"):
            nmap_Flg = 'N'
        else:
            nmap_Flg = "Y"
    if geo_Flg != "N":
        if ver[0] == "3":
            ans = input('[.] Use Geo - default Yes: ').upper()
        else:
            ans = raw_input('[.] Use Geo - default Yes: ').upper()
        if (ans == "" or ans == "Y"):
            geo_Flg = 'Y'
        else:
            geo_Flg = "N"

##    user_listen_timeout = float(input('Listen Timeout: '))
##    user_thread_timeout = float(input('Thread Timeout: '))
##    setdefaulttimeout(user_listen_timeout)
##    setdefaulttimeout(100)
    stdout.write('\n[!] Starting........\n')
    tgtPorts = str(tgtPort).split(',')
    start_time2 = time.time()
    start_time = time.clock()
    portScan(tgtHost, tgtPorts)
    
    stop_time2 = time.time()
    stop_time = time.clock()
    elapsed_time = stop_time - start_time
    elapsed_time_unix = stop_time2 - start_time2
    formated_time = parseTime(elapsed_time)
    formated_time_unix = parseTime(elapsed_time_unix)
 #   if Thread_Flg == "N":
    if _platform == "linux" or _platform == "linux2":
        stdout.write('\n[+] Run Time Unix: %s' % formated_time_unix)    # linux
    elif _platform == "darwin":
        stdout.write('\n[+] Run Time OSX: %s' % formated_time_unix)    # OS X
    elif _platform == "win32":
        stdout.write('\n[+] Run Time Windows: %s' % formated_time)
    if log_Flg.lower() == 'y':
        saveList2Log()
        stdout.write('\n[+] Results Logged')
    stdout.write('[!] Done\n')

if __name__ == '__main__':
    main()