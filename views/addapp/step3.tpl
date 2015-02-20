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
<h1>Step 3</h1>
<h2>parse input file</h2>
<p>choose how to parse this file:</p>
<form method="post" action="/addapp/step4">
    <select name="input_format">
        <option value="namelist">namelist.input
        <option value="ini">INI file
        <option value="xml">xml file
    </select>
    <input type="hidden" name="appname" value="{{appname}}">
    <input type="submit" class="btn" value="Parse">
</form>

<hr>

<pre>
{{!contents}}
</pre>
</div>

%include('footer')
