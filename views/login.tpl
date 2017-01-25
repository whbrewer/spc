%include('header')

<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id" content="{{oauth_client_id}}">

<script>
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail());

  var id_token = profile.id_token;

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/tokensignin');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    console.log('Signed in as: ' + xhr.responseText);
    if (xhr.responseText == "oauth") {
       //window.location.href = "/apps"
       continue
    }
  };

  xhr.send('idtoken=' + id_token);
  //window.location.href = "/apps"
}
</script>

<a href="#" onclick="signOut();">Sign out</a>
<script>
  function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
  }
</script>


<body>

<center>

<h3>Sign in with Google account</h3>

<div class="g-signin2" data-onsuccess="onSignIn"></div>

<hr>

</center>



<!--
<div class="row">

    <div class="col-xs-12 col-sm-6 col-md-3">
        <a class="btn btn-block btn-social btn-twitter">
            <span class="fa fa-twitter"></span> Sign in with Twitter
        </a>

        <a class="btn btn-block btn-social btn-facebook">
            <span class="fa fa-facebook"></span> Sign in with Facebook
        </a>

        <a class="btn btn-block btn-social btn-google">
            <span class="fa fa-google"></span> Sign in with Google
        </a>
    </div>

    <div class="col-sm-6 col-md-9"></div>

</div>

<hr>
-->

<div class="main left">

    <h3 align="center">Sign in with SPC account</h3>
    <!-- <h2 align="center">Sign in</h2> -->

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

    <hr>
    <p align="center">Don't have an account?
    <a class="btn btn-link" href="/register">Sign up</a></p>

</div>

</body>
</html>
