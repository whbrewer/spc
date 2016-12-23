%include('header')

<script>
function checkUser(user) {
   if (user.length == 0) { 
      $("#user_div").toggleClass('has-success', false);
      return false;
   }
   
   jQuery.ajax({
      type: "POST",
      url:  "/check_user", 
      data: { user: user },
      complete: function(xhr){
         var response = eval(xhr.responseText);
         if (response) {
            $("#user_div").toggleClass('has-error', true);
            $("#user_div").toggleClass('has-success', false);
            $("#user").select()
            $("#submit").prop('disabled', true)
            document.getElementById("username_feedback").innerText = "ERROR: username is already taken.";
         } else {
            document.reg_form.password1.focus()
            $("#user_div").toggleClass('has-error', false);
            $("#user_div").toggleClass('has-success', true);
            $("#submit").prop('disabled', false)
            document.getElementById("username_feedback").innerText = "";
         }
      }
   })
}

function checkPassword(pw) {
  var msg = "";
  var nerrors = 0;

  if (pw.length == 0) { return false }

  if (pw.length < 7) {
    msg += "ERROR: password must be at least 7 characters. ";
    nerrors += 1;  
  } else if (pw === pw.toLowerCase()) {
    msg += "ERROR: password doesn't contain any uppercase characters. ";
    nerrors += 1;
  } else if (pw.search(/[0-9]/) < 0) {
    msg += "ERROR: password must have at least one digit (e.g. 0-9). ";
    nerrors += 1;
  }

  if (nerrors > 0) {
    $("#pw1_div").toggleClass('has-error', true);
    $("#pw1_div").toggleClass('has-success', false);
    $("#submit").prop('disabled', true)
  } else {
    $("#pw1_div").toggleClass('has-error', false);
    $("#pw1_div").toggleClass('has-success', true);
    $("#submit").prop('disabled', false)
  }

  document.getElementById("pw1_feedback").innerText = msg;
}

function checkPasswordMatch() {
    if($("#password1").val() == $("#password2").val()) {
        $("#pw2_div").toggleClass('has-error', false);
        $("#pw2_div").toggleClass('has-success', true); 
        $("#submit").prop('disabled', false)
        document.getElementById("pw2_feedback").innerText = "";
        return true;
    } else {
        $("#pw2_div").toggleClass('has-error', true);
        $("#pw2_div").toggleClass('has-success', false);
        $("#submit").prop('disabled', true)
        document.getElementById("pw2_feedback").innerText = "ERROR: passwords do not match";
        return false;
    }
}

function checkEmail(email) {
    if (email.length == 0) { 
      $("#email_div").toggleClass('has-success', false);
      return false;
    }

    re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    // regex is a variation of the official standard: RFC 5322
    // see http://www.regular-expressions.info/email.html
    // re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b/

    matches = email.search(re)
    if (matches < 0) {
      document.getElementById("email_feedback").innerText = "ERROR: incorrect e-mail format";
      $("#email_div").toggleClass('has-error', true);
      $("#email_div").toggleClass('has-success', false);
    } else {
      document.getElementById("email_feedback").innerText = "";
      $("#email_div").toggleClass('has-error', false);
      $("#email_div").toggleClass('has-success', true);   
    }
}

function validateForm() {
    if( $("#user_div" ).hasClass( "has-success" ) && $("#pw1_div").hasClass("has-success") && $("$pw2_div").hasClass("has-success") && $("#email_div").hasClass("has-success") && ($("#password1").val() == $("#password2").val())) {
        return true;
    } else {
        document.getElementById("warning").innerText = "ERROR: correct errors and try again";
        return false;
    }

    // if($("#password1").val() == $("#password2").val()) {
    //     return true;
    // } else {
    //     //alert("passwords do not match")
    //     return false;
    // }
}
</script>

<style>
    input[type="text"], input[type="password"] { 
      background-color: #faffbd; 
      width: 200px;
    }
</style>

<body>
<div id="warning" align="center" class="alert-danger"></div>

<div class="main left">
    <h1>Register</h1>
    <form class="form-horizontal" name="reg_form" action="/register" method="post" onsubmit="return validateForm()">

      <div id="user_div" class="form-group">
        <label for="username" class="control-label col-md-3">Username:</label>
        <div class="col-md-9">
          <input class="form-control" id="cname" type="text" name="user" id="user" onchange="checkUser(this.value)">
          <span class="has-error" id="username_feedback"></span>
        </div>
      </div>

      <div id="pw1_div" class="form-group">
        <label for="password1" class="control-label col-md-3">Password:</label>
        <div class="col-md-9">
          <input class="form-control" type="password" name="password1" id="password1" onkeyup="checkPassword(this.value)">
          <span id="pw1_feedback"></span>
        </div>
      </div>

      <div id="pw2_div" class="form-group">
        <label for="password2" class="control-label col-md-3">Retype Password:</label>
        <div class="col-md-9">
          <input class="form-control" type="password" name="password2" id="password2" onkeyup="checkPasswordMatch()">
          <span id="pw2_feedback"></span>
        </div>
      </div>

      <div id="email_div" class="form-group">
        <label for="email" class="control-label col-md-3">Email:</label>
        <div class="col-md-9">
          <input class="form-control" type="text" name="email" id="email" onkeyup="checkEmail(this.value)">
          <span id="email_feedback"></span>
        </div>
      </div>

      <input class="btn btn-primary" type="submit" id="submit" value="Register" class="btn">
    </form>
</div>

<script>
$().ready(function() 
{ 
// validate the comment form on submission
$("#reg_form").validate(); 
}); 
</script>

</body>
</html>
