import sys
import nmap
import optparse
import os
sys.path.append(os.path.realpath('../scripts'))
from Args import *

def nmapScan(tgtHost, tgtPort):
    nmSacan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print ' [*] ' + tgtHost + ' tcp/' + tgtPort + ' ' + state

def main():
    args = Args({'-H': 'tgtHost', '-p': 'tgtPort' })
    options = args.getArgs()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(', ')
    for tgtPort in tgtPorts:
        nmapScan(tgtHost, tgtPort)
        
if __name__ == "__main__":
    main()
