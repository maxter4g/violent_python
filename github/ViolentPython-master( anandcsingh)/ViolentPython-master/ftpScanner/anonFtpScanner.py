import ftplib

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print '\n[*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded.'
        return ftp
    except Exception, e:
        print '\n[-] ' + str(hostname) + ' FTP Anonymous Logon Failed.'
        return None

# http://www.ftp-sites.org/
host = 'ftp.ch.freebsd.org'
#ftp = anonLogin(host)
#ftp.quit()
