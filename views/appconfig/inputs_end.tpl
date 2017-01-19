%include("header")

<div class="container-fluid">
<h3>Finished!</h3>

<h4>Template file successfully written.</h4>

<!-- <p>You may test the app <a href="/{{appname}}">here</a></p> -->

<p>Redirecting to <a href="/app/{{appname}}">app configuration page</a></p>

<meta http-equiv="refresh" content="1; url=/app/{{appname}}">


</font>

</div>

%include('footer')
