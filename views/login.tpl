%include('header')

%if defined('oauth_client_id'):
    <script src="https://apis.google.com/js/platform.js" async defer></script>
    <meta name="google-signin-client_id" content="{{oauth_client_id}}">
%end

<script>
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile()
  console.log('ID: ' + profile.getId()) // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName())
  console.log('Image URL: ' + profile.getImageUrl())
  console.log('Email: ' + profile.getEmail())

  var email = profile.getEmail()

  var xhr = new XMLHttpRequest()
  xhr.open('POST', '/tokensignin')
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
  xhr.onload = function() {
     console.log('Signed in as: ' + xhr.responseText)
     if (xhr.responseText) {
        window.location.href = "/myapps"
     }
  }

  xhr.send('email=' + email);
}
</script>


<body>


<h3 align="center">Sign in with SPC</h3>

<div style="height:10px"></div>

<form class="form-horizontal" action="/login" method="post">
<div class="form-group">
    <div class="col-xs-12 col-sm-offset-4 col-sm-4">
	<div class="input-group">
	    <div class="input-group-addon">
		<span class="glyphicon glyphicon-user"></span>
	    </div>
	    <input type="text" class="form-control input-lg" name="user" id="user" placeholder="username" />
	</div>
    </div>
    <div class="col-sm-6 col-md-9"></div>
</div>

<div class="form-group">
    <div class="col-xs-12 col-sm-offset-4 col-sm-4">
	<div class="input-group">
	    <div class="input-group-addon">
	       <span class="glyphicon glyphicon-lock"></span>
	    </div>
	    <input type="password" class="form-control input-lg" name="passwd" id="passwd" placeholder="password" />
	</div>
    </div>
    <div class="col-sm-6 col-md-9"></div>
</div>

<div class="form-group">
    <div class="col-xs-12 col-sm-offset-4 col-sm-4">
	<input class="btn btn-primary col-xs-12" type="submit" value="Sign in" class="btn">
    </div>
</div>

<!--<a href="/forgot">Forgot your password?</a><br>-->
<!--<input type="checkbox" name="ssi"> Stay signed in<br>-->
<input type="hidden" name="referrer" value="{{referrer}}">
</form>

<p align="center">Don't have an account?
<a class="btn btn-link" href="/register">Sign up</a></p>

%if defined('oauth_client_id'):

   <center>

   <hr>

   <h3>Or sign in with Google</h3>

   <div class="g-signin2" data-onsuccess="onSignIn"></div>
   <br>


   </center>

%end


</body>
</html>
