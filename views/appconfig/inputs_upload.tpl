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

<h4>Upload input file</h4>

<font size="+1" color="blue">
<p>Upload 
%if input_format == "namelist":
    an input file named <b><tt>{{appname}}.in</tt></b>
%elif input_format == "ini":
    an input file named <b><tt>{{appname}}.ini</tt></b>
%elif input_format == "xml":
    an input file named <b><tt>{{appname}}.xml</tt></b>
%elif input_format == "yaml":
    an input file named <b><tt>{{appname}}.yaml</tt></b>
%else:
    an input file named <b><tt>{{appname}}.json</tt></b>
%end
</p></font>

<font size="+1">
<p>Your app must be able to read and parse a text input file with
the input parameters.</p>
</font>

<form action="/appconfig/inputs/parse" method="post" enctype="multipart/form-data">
  <font size="+1">Select a file:</font> 

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
