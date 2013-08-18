import sys

import crypt


def crack(hash):
    salt = hash[0:2]
    file = open('dictionary.txt','r')
    for word in file.readlines():
        word = word.strip('\n')
        if crypt.crypt(word,'hx') == hash:
            print '[+] The password is: ',word
            return 
    print '[-] Password not found.' 


def main():
    file = open('passwords.txt','r')

if __name__ == "__main__":
    print crypt.crypt('egg','hx')
    crack('hxokzx4Ngzx5I')
