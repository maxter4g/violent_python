import socket
import sys
import os
def retBanner(ip, port):
    try:
        print "Connecting to " + ip + ": " + str(port)
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        print "Connected to " + ip + ": " + port
        banner = s.recv(1024)        
        return banner
    except Exception, e:
        print "[-] Error: " + str(e)  
        return

def checkVuls(banner, filename):
    banner = banner.strip('\n')
    f = open("vul.txt", "r")
    for line in f.readlines():
        if line.strip("\n") in banner:
            print "[+] " + banner.strip("\n") + " is vulnerable"
            

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print "[-] " + filename + " does not exist"
            exit(0)
        if not os.access(filename, os.R_OK):
            print "[-] " + filename + " access denied"
            exit(0)
    else:
        print "[-] Usage: " + str(sys.argv[0]) + " <vuln filename>"
        exit(0)
    #filename = "vul.txt"
    portList = [21, 22, 25, 80, 110, 443]
    for x in range(145, 150):
        ip = "192.168.0." + str(x)
        for port in portList:
            banner = retBanner(ip, port)
            if banner:
                print "[-] " + ip + ": " + banner
                checkVuls(banner, filename)


if __name__ == '__main__':
    main()
    
