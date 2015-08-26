<!DOCTYPE html>
<html>
<head>
<link rel="Stylesheet" href="/static/css/bootstrap.min.css" />
<script src="/static/jquery-2.1.4.min.js"></script>
<script src="/static/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container-fluid">
<h3>Configure Executable: step 1 of 2</h3>

<br>

<h4>Upload Executable File</h4>

<font size="+1">

<p>Upload binary file that is compatible to run on the host platform:</p>

</font>

<form action="/appconfig/exe/test" method="post" enctype="multipart/form-data">
  <font size="+1">Select a file:</font> 

  <input type="file" class="btn btn-default btn-file" name="upload"><br>
  <input type="hidden" name="appname" value="{{appname}}">
  <input type="submit" value="Next >>" class="btn btn-primary"/>
</form>
</div>

%include('footer')
