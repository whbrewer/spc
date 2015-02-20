<!DOCTYPE html>
<html>
<head>
<link type="text/css" rel="Stylesheet" href="/static/css/login.css"   />
<link type="text/css" rel="StyleSheet" href="/static/css/navbar.css"  />
<link type="text/css" rel="StyleSheet" href="/static/css/default.css" />
</head>

<body>

%include('addapp/navbar')

<div class="main left">
<h1>Finished!</h1>

<p><font size="+1">Template file successfully written.</p>
You may test the app here:</p>

<a href="http://localhost:8081/{{appname}}">localhost:8081/{{appname}}</a>

</font>

<!--
<form method="post" action="/addapp/step6">
   <input type="submit" value="load apps">
</form>
-->

</div>

%include('footer')
