'''
tested on linux python 2 and 3

todo:

verify other tag

'''

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
ver = sys.version.split(' ')[0]
if ver[0] == "3":
    import urllib
else:
    import urllib2
    from urlparse import urlsplit
from PIL import Image #install pillow for Python 3
from PIL.ExifTags import TAGS
from sys import stdout
from os.path import basename
from bs4 import BeautifulSoup
 

def findImages(url):
    try:
        stdout.write( '[+] Seeking images on ' + url)
        stdout.flush()
        ver = sys.version.split(' ')[0]
        if ver[0] == "3":
            urlContent = urllib.request.urlopen(url)
        else:
            urlContent = urllib2.urlopen(url).read()
        soup = BeautifulSoup(urlContent)
        imgTags = soup.findAll('img')
        return imgTags
    except Exception as e:
        if verbose_Flg == 'N':
            stdout.write('\n[-] Err: %s' % e)
            stdout.write('\n')
            stdout.write('\n[!] Done ')
            stdout.flush()
            exit(0)

def downloadImage(imgTag):
    try:
        imgSrc = imgTag['src']
        ver = sys.version.split(' ')[0]
        if ver[0] == "3":
            imgContent = urllib.request.urlopen(imgSrc)
            imgFileName = basename(urllib.parse.urlsplit(imgSrc)[2])
            if imgFileName[-3:] == "jpg":
                __dir__ = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(__dir__, 'tmpImg/' + imgFileName)
                imgFile = open(filepath, 'wb')
                imgFile.write(imgContent.read())
                stdout.write( '\n[+] Dowloading image...')
                imgFile.close()
                stdout.write(' ' + imgFileName )
                stdout.flush()
                return filepath
        else:
            imgContent = urllib2.urlopen(imgSrc).read()
            imgFileName = basename(urlsplit(imgSrc)[2])
            if imgFileName[-3:] == "jpg":
                __dir__ = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(__dir__, 'tmpImg/' + imgFileName)
                imgFile = open(filepath, 'wb')
                imgFile.write(imgContent)
                stdout.write( '\n[+] Dowloading image...')
                imgFile.close()
                stdout.write(' ' + imgFileName )
                stdout.flush()
                return filepath
    except Exception as e:
        stdout.write('\n[-] Err: %s' % e)
        stdout.write('\n')
        stdout.flush()
        return ''

def testForExif3(imgFileName):
    try:
        tags = {}
        tags = exifread.process_file(f)
        for tag in tags.keys():
             if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                 print("Key: %s, value %s" % (tag, tags[tag]))
    except Exception as e:
        stdout.write('\n[-] Err: %s' % e)
        stdout.write('\n')
        stdout.flush()
        pass



def testForExif(imgFileName):
    global verbose_Flg
    try:
        exifData = {}
        imgFile = Image.open(imgFileName)
        info = imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifData[decoded] = value
            exifGPS = exifData['GPSInfo']
            if exifGPS:
                stdout.write( '\n[*] ' + imgFileName + ' contains GPS MetaData')
                stdout.write('\n')
    except Exception as e:
        if verbose_Flg == 'Y':
            stdout.write('\n[-] Err: %s' % e) 
            stdout.write('\n')
            stdout.flush()
        pass

def main():
    global verbose_Flg
    ver = sys.version.split(' ')[0]
    if ver[0] == "3":
        anst = input('[.] Target domain(www.example.com): ')
#        ansv = input('[.] Verbose - default Y: ').upper()
    else:
        anst = raw_input('[.] Target domain(www.example.com): ')
#        ansv = raw_input('[.] Verbose - default Y: ').upper()
    if anst == "":
        url = 'http://www.flickr.com/photos/dvids/4999001925/sizes/o'
    elif anst == "ddd":
        url = 'http://www.tiscali.it'
    else:
        url = "http://" + anst
 #   verbose_Flg = 'Y' if (ansv == "" or ansv == "Y") else "N"
    verbose_Flg = 'N'
#    stdout.write('\n[!] Starting........\n')
    count = 0
    imgTags = findImages(url)
    for imgTag in imgTags:
        imgSrc = imgTag['src']
        if (imgSrc[-4:]== '.jpg' and imgSrc[0:4] == 'http'):
            count += 1
            imgFileName = downloadImage(imgTag)
            ver = sys.version.split(' ')[0]
            if ver[0] == "3":
                testForExif(imgFileName) #use testForExif3 for exifread
            else:
                testForExif(imgFileName)
        else:
            pass
    if count > 0:
        stdout.write('\n[!] Done ')
        stdout.write(' %s image(s) Found\n' % str(count))    
    else:
        stdout.write('\n[!] Done NO jpg images Found\n')

if __name__ == '__main__':
    main()
