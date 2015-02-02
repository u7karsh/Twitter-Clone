#!/usr/bin/env python
import sys
import cgitb, cgi

#import libw from one dir back
sys.path.insert(0, '../')
import lib_web as libw

cgitb.enable()
form=cgi.FieldStorage()

if ("q" in form):
	user = cgi.escape(form["q"].value)
else:
	user = libw.getUser()

user = user.lower()
ret = libw.auth_cookie()
print "Content-type: text/html\n\n"

if ret == 0:
	print '<meta http-equiv="refresh" content="0;url=http://localhost" />'
else:

	print '''
<!DOCTYPE HTML>
<html>
<head>
<title>Twitter Clone Profile</title>
<link href="css/bootstrap.css" rel='stylesheet' type='text/css' media="all" />
<script src="js/jquery-1.11.0.min.js"></script>

<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/themes/smoothness/jquery-ui.css" />
<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js"></script>

<link href="css/style.css" rel='stylesheet' type='text/css' media="all" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<script type="application/x-javascript"> addEventListener("load", function() { setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } </script>
<link href='http://fonts.googleapis.com/css?family=Lato:100,300,400,700,900' rel='stylesheet' type='text/css'>
<link rel="stylesheet" href="css/sticky-navigation.css" />
<link href="css/demo.css" rel="stylesheet" type="text/css" />
<script>
$(function() {

// grab the initial top offset of the navigation 
var sticky_navigation_offset_top = $('#sticky_navigation').offset().top;

// our function that decides weather the navigation bar should have "fixed" css position or not.
var sticky_navigation = function(){
var scroll_top = $(window).scrollTop(); // our current vertical position from the top

// if we've scrolled more than the navigation, change its position to fixed to stick to top, otherwise change it back to relative
if (scroll_top > sticky_navigation_offset_top) { 
$('#sticky_navigation').css({ 'position': 'fixed', 'top':0, 'left':0 });
} else {
$('#sticky_navigation').css({ 'position': 'relative' }); 
}   
};

// run our function on load
sticky_navigation();

// and run it again every time you scroll
$(window).scroll(function() {
sticky_navigation();
});

// NOT required:
// for this demo disable all links that point to "#"
$('a[href="#"]').click(function(event){ 
event.preventDefault(); 
});

});
</script>
</head>
<body>
<!-- Header Part Starts Here -->
<div class="header">
<div class="container">
<div id="demo_top_wrapper">
<div id="sticky_navigation_wrapper">
<div id="sticky_navigation">
<div class="demo_container navigation-bar">
<div class="navigation">
<div class="logo"><a href="index.html">TC</a></div>
<span class="menu"></span>
<script>
$( "span.menu" ).click(function() {
$( ".navig" ).slideToggle( "slow", function() {
// Animation complete.
});
});
</script>
<div class="navig">
<ul>
<li><a href="index.py">Home</a></li>
<li><a href="profile.py">Profile</a></li>
<li><a href="follower.py">Following</a></li>
<li><a href="discover.py">Discover</a></li>
</ul>
</div>
<div class="clearfix"></div>

</div>
<div class="navigation-right">

<ul class="user">
<button id="clickMe"> Tweet</button>
<a href="logout.py"><button id="logout"> Logout</button></a>
</ul>

</div>
<!-- for tweet input box  -->	
<div id="myDialog">
Tweet-Clone Box 
<textarea id="textarea" rows="3" cols="20" maxlength="99" ></textarea>
<div id="textarea_feedback"></div>
</div>


<div class="clearfix"></div>
<div class="serch">
<span>
<input type="text" placeholder="Search" required="">
<input type="submit" value="" />
</span>
</div>
<script>
$( "button.search" ).click(function() {
$( ".serch" ).slideToggle( "slow", function() {
// Animation complete.
});
});
</script>
<div class="clearfix"></div>
</div>
</div>
</div>
</div>
</div>
</div>
<div class="container">
<section id="main">

<div class="content">
<div class="gallery">
<div class="twit t-wit-user">
<p>'''
	#getting the details of the login user from users table and showing in the left box 
	cur = libw.sql_query("SELECT email from `users` where `user` = '" + str(user) + "'")
	row = cur.fetchone()
	if row is not None:
		print row[0]
		print '</p><small>@'+str(user)+'</small></div>'
		if not user == libw.getUser():
			cur = libw.sql_query("SELECT follow from `follows` where `user` = '" + str(libw.getUser()) + "' and `follow` = '"+str(user)+"'")
			if cur.rowcount > 0:
				print '<a href="addFollow.py?a=unfollow&q='+str(user)+'"><button class="followbtn">Un Follow</button></a>'
			else:
				print '<a href="addFollow.py?q='+str(user)+'"><button class="followbtn">Follow</button></a>'
	else:
		print "User Not Found!!</p></div>"

	#showing all the tweets of the login user in decreasing order timestamp
	cur = libw.sql_query("SELECT * from `tweets` where `user` = '" + str(user) + "' ORDER BY timestamp DESC")
	for row in cur.fetchall():
		print '''
			<div class="twit t-wit">
			<span class="line"></span>
			<i class="twit-icon"></i>
			<span class="line"></span>
			<div style="text-align: right;color:#fff">'''
		print str(row[3])+'</div><p>'#timestamp
		print row[2]#tweet
		print "</p><small><a href='profile.py?q="+str(row[1])+"'>@"+str(row[1])+"</a></small></div>"
	print '''
</div>
</div>
</div>
</section>
</div>

</body>
<script >

//Set up the dialog box
$("#myDialog").dialog({
autoOpen  : false,
modal     : true,
title     : "A Dialog Box",
buttons   : {
'Tweet' : function() {
var textValue = $('#textarea').val();
if (window.XMLHttpRequest) {
// code for IE7+, Firefox, Chrome, Opera, Safari
xmlhttp = new XMLHttpRequest();
} else {
// code for IE6, IE5
xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}
xmlhttp.onreadystatechange = function() {
if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
//acknowledgement
}
}
xmlhttp.open("GET","statusUpdate.py?q="+textValue,true);
xmlhttp.send();
$(this).dialog('close');
//Now you have the value of the textbox
},
'Close' : function() {
$(this).dialog('close');
}
}
});

$('#clickMe').click(function() {
$("#myDialog").dialog("open");
});

$(document).ready(function() {
var text_max = 99;
$('#textarea_feedback').html(text_max + ' characters remaining');

$('#textarea').keyup(function() {
var text_length = $('#textarea').val().length;
var text_remaining = text_max - text_length;

$('#textarea_feedback').html(text_remaining + ' characters remaining');
});
});

</script>


</html>'''