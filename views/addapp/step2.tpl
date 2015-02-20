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
<h1>Step 2</h1>

<h2>Upload zip file</h2>

<font size="+1">
<p>The file must be a <b><tt><u>zip</u></tt></b> file, 
which contains the following files:</p>
<ol>
%if input_format == "namelist":
<li> an input file named <b><tt>{{appname}}.in</tt></b>
%else:
<li> an input file named <b><tt>{{appname}}.ini</tt></b>
%end
<li> a Linux binary file called <b><tt>{{appname}}</tt></b>
</ol>

<p>Your app must be able to read and parse a text input file with
the input parameters.</p>
</font>

<form action="/addapp/step3" method="post" enctype="multipart/form-data">
  <!-- Category: <input type="text" name="category" /> -->
  <font size="+1">Select a zip file:</font> 
  <input type="file" name="upload" />
  <input type="hidden" name="appname" value="{{appname}}">
  <input type="submit" value="Next >>" class="btn"/>
</form>
</div>

%include('footer')
