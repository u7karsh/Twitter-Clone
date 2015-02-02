#!/usr/bin/env python
import sys
import cgitb

#import libw from one dir back
sys.path.insert(0, '../')
import lib_web as libw

cgitb.enable()

#destroying the cookie (logout)
print libw.deAuth()
print "Content-type: text/html\n\n"
print '<meta http-equiv="refresh" content="0;url=http://localhost" />'