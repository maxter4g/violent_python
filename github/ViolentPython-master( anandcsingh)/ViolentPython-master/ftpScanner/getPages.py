import ftplib
def getFtpPages(ftp):
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        print '[-] Could not list directory contents.'
        print '[-] Skipping to Next Target.'
        return
    retList = []
    pageFileTypes = ['.php', '.htm', '.asp', '.aspx']
    for fileName in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn or '.aspx' in fn:
            print '[+] Found web page: ' + fileName
            retList.append(fileName)
    return retList

host = 'ftp.anandcsingh.com'
user = 'todotnt'
password = 'p@ssw0rd'
'''ftp = ftplib.FTP(host)
ftp.login(user, password)
print '\n[+] FTP connected'
getFtpPages(ftp)
ftp.quit()
''' 
        

