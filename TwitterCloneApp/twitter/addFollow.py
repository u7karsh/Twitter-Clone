#!/usr/bin/env python
import sys
import cgi
import cgitb
import hashlib

sys.path.insert(0, '../')
import lib_web as libw

cgitb.enable()

form=cgi.FieldStorage()

ret = libw.auth_cookie()
print "Content-type: text/html\n\n"

#follow and unFollow a person
if ret == 0:
	print '<meta http-equiv="refresh" content="0;url=http://localhost" />'
else:
	if ("a" in form) and ("q" in form):
		q = cgi.escape(form["q"].value)
		if cgi.escape(form["a"].value) == "unfollow":
			query = "delete from `follows` where `user`='" + str(libw.getUser()) + "' and `follow` = '" + str(q)+"'"
			cur = libw.sql_query(query)
			print '<meta http-equiv="refresh" content="0;url=profile.py?q='+str(q)+'" />'
		else:
			query = "insert into `follows` (`user`, `follow`) values ('" + str(libw.getUser()) + "','" + str(q)+"')"
			cur = libw.sql_query(query)
			print '<meta http-equiv="refresh" content="0;url=profile.py?q='+str(q)+'" />'
	elif ("q" in form):
		q = cgi.escape(form["q"].value)
		query = "insert into `follows` (`user`, `follow`) values ('" + str(libw.getUser()) + "','" + str(q)+"')"
		cur = libw.sql_query(query)
		print '<meta http-equiv="refresh" content="0;url=profile.py?q='+str(q)+'" />'
	else:
		print '<meta http-equiv="refresh" content="0;url=index.py" />'
