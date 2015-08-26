<!DOCTYPE html>
<html>
<head>
<link rel="Stylesheet" href="/static/css/bootstrap.min.css" />
<script src="/static/jquery-2.1.4.min.js"></script>
<script src="/static/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container-fluid">
<h3>Configure inputs: step 1 of 3</h3>

<br>

<h4>Upload zip file</h4>

<font size="+1">
<p>Upload a Zip file named <b><tt>{{appname}}.zip</tt></b>,
which contains the following files:</p>
<ol>
%if input_format == "namelist":
    <li> an input file named <b><tt>{{appname}}.in</tt></b>
%else:
    <li> an input file named <b><tt>{{appname}}.ini</tt></b>
%end
<li> an executable file called <b><tt>{{appname}}</tt></b>, 
     along  with any necessary supporting files 
</ol>

<p>Your app must be able to read and parse a text input file with
the input parameters.</p>
</font>

<form action="/inputs/edit/parse" method="post" enctype="multipart/form-data">
  <!-- Category: <input type="text" name="category" /> -->
  <font size="+1">Select a zip file:</font> 

  <input type="file" class="btn btn-default btn-file" name="upload"><br>
  <!-- see http://stackoverflow.com/questions/11235206/twitter-bootstrap-form-file-element-upload-button
  <span type="file" class="btn btn-default btn-file" name="upload">
  	Browse<input type="file">
  </span>
	-->
  	<br>
  <input type="hidden" name="appname" value="{{appname}}">
  <input type="hidden" name="input_format" value="{{input_format}}">
  <input type="submit" value="Next >>" class="btn btn-primary"/>
</form>
</div>

%include('footer')
