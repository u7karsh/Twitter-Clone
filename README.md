# Twitter-Clone
Twitter Clone


### Introduction 
-----
A python based twitter like web application. This app enables user to login their account and do some basic twitter like operations. Backend developed by Utkarsh Mathur (@U7karsh) and front end by Siddharth Dimania

### Quick Setup
-----
1.Installing Python web environment 
	link : http://www.programcreek.com/2012/04/python-hello-world-web-application-in-ubuntu/

2.CGI scripts in Python
	link : http://raspberrywebserver.com/cgiscripting/writing-cgi-scripts-in-python.html

3.Copy default file from the setup folder to  
	sudo vi /etc/apache2/sites-available/default

4.Copy the Content of the folder TwitterClone App into folder /usr/lib/cgi-bin/ 

5.Create a dabase name twitter_clone and import the sql file from the the sqlFile Folder.  

6.Go to your browser and run localhost(phpmyadmin and mysql already installed)

**NOTE**: Tested ON Ubuntu 12.04/14.04

**NOTE**: If not able to run .py files check for python-mysqldb and python-request

### Login and Register Form
-----
login and register the user 

**NOTE**: if you don't want to register , use test username and password from the Folder TestUserPass

### User Profile 
-----
* Home (showing the tweets of all the user's following people)
* Profile (showing the login user details(on the left box) and all the tweets of the login user)
* Following (showing the following users of the current login user)
* Discover (showing all the tweets)

**NOTE**: There is Follow and UnFollow button on the right side of the following user's profile.

### Main ( py File )
-----

1. main python file 
	* lib_web.py is the library that contains functions like getUser , save_cookie , regUser etc.

### Sql Tables
-----
* users (all the registered users) ->
| id 	| user   | email   | timestamp

* tweets ( all the tweets of users) -> 
| id 	| user   | tweet  | timestamp

* follows (follow user table) ->
| id 	| user   | follow  |

* Cookie

* auth

### Sql queries 

* Home Page :

select Distinct f.user, u.user, t.tweet, t.timestamp from users inner join follows f on (f.user = "'+str(libw.getUser())+'") inner join users u on (u.user= f.follow) inner join tweets t on (t.user = f.follow) ORDER BY t.timestamp DESC'

str(libw.getUser()) : getting current login user

**NOTE**: getting following user's tweets and showing on the timeline  

* Profile Page : 

SELECT * from `tweets` where `user` = '" + str(user) + "' ORDER BY timestamp DESC"

str(user): current login user

* Following Page : 

select Distinct f.user, u.user from users inner join follows f on (f.user = "'+str(libw.getUser())+'") inner join users u on (u.user= f.follow)'

* Discover Page : 

SELECT * from `tweets` ORDER BY timestamp DESC"

### MySql Replication
-----
* link : http://www.mysql.com/products/enterprise/replication.html

For the scalability of this System 











