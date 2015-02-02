#!/usr/bin/env python
import lib_web as libw
import cgi
import cgitb
import hashlib

cgitb.enable()

form=cgi.FieldStorage()

if ("username" not in form) and ("password" not in form):
	### start header followed by body as no header mod required here ###
	print "Content-type: text/html\n\n"
	print '<meta http-equiv="refresh" content="0;url=http://localhost" />'
else:
	### start header from here ###
	user = cgi.escape(form["username"].value)
	if not ("loginkeeping" not in form):
		print libw.save_cookie(user, 1)
	else:
		print libw.save_cookie(user, 0)

	### start body from here ###
	passwd =  hashlib.sha224(str(cgi.escape(form["password"].value))).hexdigest()
	print "Content-type: text/html\n\n"
	if libw.auth( user, passwd) == 1:
		print '<meta http-equiv="refresh" content="0;url=twitter/index.py" />'
	else:
		print "</br>Invalid username or password"
