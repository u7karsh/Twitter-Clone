#!/usr/bin/env python
import cgi
import sys
import cgitb

#import libw from one dir back
sys.path.insert(0, '../')
import lib_web as libw

cgitb.enable()

# adding tweet into the tweets table
form=cgi.FieldStorage()
print "Content-type: text/html\n\n"
ret = libw.auth_cookie()
if ret == 1:
	if ("q" not in form):
		print 'Failed to update status'
	else:
		cur = libw.sql_query('insert into `tweets` (`user`, `tweet`) values ("'+str(libw.getUser())+'","'+str(cgi.escape(form["q"].value))+'")')
else:
	print 'Failed to update status'