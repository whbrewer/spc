<!DOCTYPE html>
<html>
<head>
<link type="text/css" rel="Stylesheet" href="/static/css/login.css"   />
<link type="text/css" rel="StyleSheet" href="/static/css/navbar.css"  />
<link type="text/css" rel="StyleSheet" href="/static/css/default.css" />
</head>

<body>

%include('addapp/navbar')

<div class="left main">
<h1>Step 1</h1>
<h2>configure app</h2>
<form action="/addapp/step2" method="post">
<input type="hidden" name="appname" value="{{appname}}">
<input type="hidden" name="user" value="{{user}}">

<table>
<tr>
<td><font size="+1">Description:<br>
    <font size="-1">80 chars max</font></font></td>
<td><textarea name="description" cols=40 rows=2></textarea></td>

<tr>
<td><font size="+1">Tags:</font><br>
    <font size="-1">e.g. Bioinformatics</font></td>
<td><input type="text" name="category"></td>
<!--
<td><select name="category" onchange="somefn()">
   <option SELECTED value="bioinformatics">Bioinformatics
   <option value="bioinformatics">Bioinformatics
   <option value="cfd">CFD
   <option value="other">Other
</select></td>
-->
</tr>

<!--
<tr>
<td>Language:</td>
<td><select name="language">
   <option value="c">c
   <option value="C++">C++
   <option value="fortran">Fortran
   <option value="fortran">Fortran90
   <option value="java">Java
   <option SELECTED value="python">Python
   <option value="ruby">Ruby
</select></td>
</tr>
-->

<tr>
<td>Input format:</td>
<td><select name="input_format">
   <option SELECTED value="namelist">Namelist
   <option value="ini">INI
   <option value="xml">XML
</select></td>
</tr>

<tr>
<td><font size="+1">Command to run app:</font><br> 
<font size="-1">Note: this is a relative path from the <tt>user_data/app/user</tt> directory</font></td>
<td><input type="text" name="command" value="../../../../apps/{{appname}}/{{appname}}"></td>
</tr>

<!--
<tr>
<td>Preprocess:</td>
<td><select name="preprocess">
   <option SELECTED value="">None
   <option value="1">Convert params to command line args
</select></td>
</tr>

<tr>
<td>Postprocess:</td>
<td><select name="postprocess">
   <option SELECTED value="">None
</select></td>
</tr>
-->

</table>
<br><input type="submit" class="btn">
</form>
</div>

%include('footer')

