#!/usr/bin/python

import bluetooth
import time

print "In/Out Board"

while True:
    print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())

    result = bluetooth.lookup_name('F0:6B:CA:AC:EB:06', timeout=5)
    if (result != None):
        print "T-Wil: in"
    else:
        print "T-Wil: out"

    result = bluetooth.lookup_name('EC:35:86:BD:75:6F', timeout=5)
    if (result != None):
        print "O-Wil: in"
    else:
        print "O-Wil: out"

    time.sleep(60)

