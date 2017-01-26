%include('header')

<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id" content="{{oauth_client_id}}">

<script>
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  //console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  //console.log('Name: ' + profile.getName());
  //console.log('Image URL: ' + profile.getImageUrl());
  //console.log('Email: ' + profile.getEmail());

  var id_token = profile.id_token;

  //var xhr = new XMLHttpRequest();
  //xhr.open('POST', '/tokensignin');
  //xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  //xhr.onload = function() {
  //  console.log('Signed in as: ' + xhr.responseText);
  //  if (xhr.responseText == "oauth") {
  //     window.location.href = "/apps"
  //  }
  //};

  //xhr.send('idtoken=' + id_token);
}

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
