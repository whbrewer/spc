<!DOCTYPE html>
<html>
<head>
<link rel="Stylesheet" href="/static/css/bootstrap.min.css" />
</head>

<body>

<div class="container-fluid">
<h1>Finished!</h1>

<p><font size="+1">Template file successfully written.</p>
You may test the app here:</p>

<p>http://<em>host</em>:{{port}}/{{appname}}</p>
<!-- See http://stackoverflow.com/questions/6016120/relative-url-to-a-different-port-number-in-a-hyperlink for how to improve this in the future -->

<p>For example:<br>
http://localhost:{{port}}/{{appname}}<br>
http://ec2-53-28-69-199.us-east-1.compute.amazonaws.com:{{port}}/{{appname}}
</p>

</font>

<!--
<form method="post" action="/addapp/step6">
   <input type="submit" value="load apps">
</form>
-->

</div>

%include('footer')
