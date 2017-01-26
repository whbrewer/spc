%include('header')

<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id" content="{{oauth_client_id}}">

<script>
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
  window.location.href = "/login"
}
</script>

<body>

<center>

<div class="g-signin2" data-onsuccess="onSignIn" style="display:none"></div>

<h2> <a href="#" onclick="signOut()">Click here to sign out</a></h2>

</center>

</body>

</html>

