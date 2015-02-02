#!/usr/bin/env python
import lib_web as libw
import cgi
import cgitb

cgitb.enable()

form=cgi.FieldStorage()
if ("usernamesignup" not in form) and ("emailsignup" not in form) and ("passwordsignup" not in form) and ("passwordsignup_confirm" not in form):
	### start header followed by body as no header mod required here ###
	print "Content-type: text/html\n\n"
	print "<h1>no post passed</h1>"
else:
	### start body from here ###
	print "Content-type: text/html\n\n"
	user = cgi.escape(form["usernamesignup"].value)
	email = cgi.escape(form["emailsignup"].value)
	passwd =  cgi.escape(form["passwordsignup"].value)
	passwd_c =  cgi.escape(form["passwordsignup_confirm"].value)
	if passwd == passwd_c:
		cur = libw.sql_query("SELECT * from `auth` where `user` = '"+str(user.lower())+"'")
		if cur.rowcount > 0:
			row = cur.fetchall()
			print "already a member"
		else:
			libw.regUser( email.lower(), user.lower(), passwd )
			print "registered!"
