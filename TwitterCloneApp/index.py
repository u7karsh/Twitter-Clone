#!/usr/bin/env python
import lib_web as libw
import cgitb

cgitb.enable()

ret = libw.auth_cookie()
print "Content-type: text/html\n\n"

if ret == 1:
	print "twitter here"
else:
	print '<meta http-equiv="refresh" content="0;url=http://localhost" />'
