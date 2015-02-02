import Cookie, os, pickle
from random import randint
import hashlib
import MySQLdb
import requests
import time

####################################################
##Fn to execute an sql query and return the result##
####################################################

def sql_query( query ):
	db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     	user="root", # your username
                      	passwd="root", # your password
                      	db="clone_twitter") # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor() 
	# Use all the SQL you like
	cur.execute(query)
	db.commit()
	return cur

####################################################
########Fn to authenticate login credentials########
####################################################

def auth( user, passwd ):
	cur = sql_query("Select * from `auth` where `user` = '" + str(user) + "'")
	if cur.rowcount > 0:
		row = cur.fetchone()
		if row[1] == passwd:
			return 1
		else:
			return 0
	else:
		return 0

####################################################
########Fn to authenticate login cookies############
####################################################
def auth_cookie():
	# The returned cookie is available in the os.environ dictionary
	cookie_string = os.environ.get('HTTP_COOKIE')
	if not cookie_string:
		return 0
	else:
		cookie = Cookie.SimpleCookie()
		# load() parses the cookie string
		cookie.load(cookie_string)
		# Use the value attribute of the cookie to get it
		user = str(cookie['user'].value)
		idd = str(cookie['id'].value)
		token = str(cookie['token'].value)
		cur = sql_query("SELECT * from `cookie` where `user` = '" + str(user) + "'")
		if cur.rowcount > 0:
			row = cur.fetchone()
			if (row[1] == idd) and (row[2] == token):
				refresh()
				return 1
			else:
				return -1 #threat detected!
		else:
			return 0

####################################################
########Fn to get username of logged in user########
####################################################
def getUser():
	# The returned cookie is available in the os.environ dictionary
	cookie_string = os.environ.get('HTTP_COOKIE')
	if not cookie_string:
		return None
	else:
		cookie = Cookie.SimpleCookie()
		# load() parses the cookie string
		cookie.load(cookie_string)
		# Use the value attribute of the cookie to get it
		user = str(cookie['user'].value)
		return user
		
####################################################
################Fn to save login cookies############
####################################################
def save_cookie( user,  state):
	idd = generateRandomString(10)
	token = generateRandomString(10)
	con = sql_query('INSERT INTO `cookie` (`user`, `id`, `token`) VALUES ("' + str(user)+'", "'+str(idd)+'", "'+str(token)+'" ) ON DUPLICATE KEY UPDATE `id`="'+str(idd)+'", `token`="'+str(token)+'"')
	if state == 1:
		lease = 30 * 24 * 60 * 60 #30 days expiry
		end = time.gmtime(time.time() + lease)
		expires = time.strftime("%a, %d %b %Y %T GMT", end)
		return 'Set-Cookie: user=' + str(user) + ' & id=' + str(idd) + ' & token=' + str(token) + '; Expires='+str(expires)+';'
	else:
		return 'Set-Cookie: user=' + str(user) + ' & id=' + str(idd) + ' & token=' + str(token)
	

####################################################
################Fn for deauthentication#############
####################################################
def deAuth():
	c=Cookie.SimpleCookie()
	c['user']=''
	c['user']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

	c['id']=''
	c['id']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

	c['token']=''
	c['token']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

	con = sql_query("DELETE from `cookie` where `user` = '"+str(getUser())+"'");
	return c


####################################################
################Fn to refresh token#################
####################################################
def refresh():
	token = generateRandomString(10)
	cookie_string = os.environ.get('HTTP_COOKIE')
	cookie = Cookie.SimpleCookie()
	# load() parses the cookie string
	cookie.load(cookie_string)
	# Use the value attribute of the cookie to get it
	user = str(cookie['user'].value)
	idd = str(cookie['id'].value)
	token = str(cookie['token'].value)
	con = sql_query('INSERT INTO `cookie` (`user`, `id`, `token`) VALUES ("'+str(user)+'", "'+str(idd)+'", "'+str(token)+'" ) ON DUPLICATE KEY UPDATE `id`="'+str(idd)+'", `token`="'+str(token)+'"')
	return 'Set-Cookie: token=' + str(token)

####################################################
################generate random string##############
####################################################

def generateRandomString(length):
	characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	randomstring = ''
	for i in range(0, length):
		randomstring = randomstring + str(characters[randint(0, 61)])

	return randomstring

####################################################
###################Register a User##################
####################################################

def regUser( email, user , passwd ):
	pass_n = hashlib.sha224(str(passwd)).hexdigest()
	sql_query('INSERT INTO `auth` (`user`, `pass`) VALUES ("'+str(user)+'", "'+str(pass_n)+'")')
	###will be extending this db in futute for storing user specific details
	sql_query('INSERT INTO `users` (`user`, `email`) VALUES ("'+str(user)+'", "'+str(email)+'")')


####################################################
############Function to the change password#############
####################################################
def changePass( user, old_pass, passwd):
	cur = sql_query('SELECT * FROM `auth` where `user` = "'+str(user)+'"')
	if cur.rowcount > 0:
		row = cur.fetchone()
		if row[1] == hashlib.sha224(str(old_pass)).hexdigest():
			resetPass( user, passwd)
			return 1
		else:
			return 0
	else:
		return 0

####################################################
#############Function to reset password#############
####################################################
def resetPass( user, passwd ):
	con = sql_query('UPDATE `auth` set `pass` = "'+hashlib.sha224(str(passwd))+'" where `user` = "'+str(user)+'"')


####################################################
#######Function to create session variables#########
####################################################
def createSession(name, value):
	s = requests.session()
	s.get('http://localhost', cookies = {str(name), str(value)})

####################################################
#######Function to return session variables#########
####################################################
def getSession(name):
	s = requests.session()
	s.get('http://localhost')
	return s.cookies

