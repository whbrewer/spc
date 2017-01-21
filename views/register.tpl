%include('header')

<script>

function fixUsername(user) {
  // re = /[\s:;`?<>,!~@#$%^&*(){}/\]/g;
  re = /[\s\W]/g;
  if (user.search(re) > 0) { 
    document.getElementById("user_comments").innerText = "special characters or spaces not allowed"
  }
  document.getElementById("user").value = user.replace(re, '')
}

function checkUser(user) {
   if (user.length == 0) { 
      $("#user_div").toggleClass('has-success', false)
      $("#user_div").toggleClass('has-error', false)
      $("#user_feedback").removeClass('glyphicon-ok')
      $("#user_feedback").removeClass('glyphicon-remove')
      document.getElementById("user_comments").innerText = ""
      return false
   } else if (user.length > 20) {
      $("#user_div").toggleClass('has-error', true)
      $("#user_div").toggleClass('has-success', false)
      $("#user_feedback").addClass('glyphicon-remove')
      $("#user_feedback").removeClass('glyphicon-ok')
      document.getElementById("user_comments").innerText = "username should be less than 20 characters"
      return false
   }

   jQuery.ajax({
      type: "POST",
      url:  "/check_user", 
      data: { user: user },
      complete: function(xhr){
         var response = eval(xhr.responseText)
         if (response) {
            $("#user_div").toggleClass('has-error', true)
            $("#user_div").toggleClass('has-success', false)
            $("#user").select()
            $("#submit").prop('disabled', true)
            $("#user_feedback").addClass('glyphicon-remove')
            $("#user_feedback").removeClass('glyphicon-ok')
            document.getElementById("user_comments").innerText = "username is already taken.";
         } else {
            document.reg_form.password1.focus()
            $("#user_div").toggleClass('has-error', false);
            $("#user_div").toggleClass('has-success', true);
            $("#user_feedback").addClass('glyphicon-ok')
            $("#user_feedback").removeClass('glyphicon-remove')
            $("#submit").prop('disabled', false)
            document.getElementById("user_comments").innerText = "";
            document.getElementById("warning").style.display = "none"
         }
      }
   })
}

function checkPassword(pw) {
  var msg = "";
  var nerrors = 0;

  if (pw.length == 0) {
    $("#pw1_div").toggleClass('has-success', false)
    $("#pw1_div").toggleClass('has-error', false)
    $("#pw1_feedback").removeClass('glyphicon-ok')
    $("#pw1_feedback").removeClass('glyphicon-remove')
    document.getElementById("user_comments").innerText = ""    
    return false
  }

  if (pw.length < 7) {
    msg += "password must be at least 7 characters. "
    nerrors += 1
  } else if (pw === pw.toLowerCase()) {
    msg += "password doesn't contain any uppercase characters. "
    nerrors += 1
  } else if (pw.search(/[0-9]/) < 0) {
    msg += "password must have at least one digit (e.g. 0-9). "
    nerrors += 1
  }

  if (nerrors > 0) {
    $("#pw1_div").toggleClass('has-error', true)
    $("#pw1_div").toggleClass('has-success', false)
    $("#submit").prop('disabled', true)
    $("#pw1_feedback").addClass('glyphicon-remove')
    $("#pw1_feedback").removeClass('glyphicon-ok')
  } else {
    $("#pw1_div").toggleClass('has-error', false)
    $("#pw1_div").toggleClass('has-success', true)
    $("#submit").prop('disabled', false)
    $("#pw1_feedback").addClass('glyphicon-ok')
    $("#pw1_feedback").removeClass('glyphicon-remove')
    document.getElementById("warning").style.display = "none"
  }

  document.getElementById("pw1_comments").innerText = msg
}

function checkPasswordMatch() {
  if(document.getElementById("password2").value.length == 0) {
    $("#pw2_div").toggleClass('has-error', false)
    $("#pw2_div").toggleClass('has-ok', false)    
    $("#pw2_feedback").removeClass('glyphicon-remove')
    $("#pw2_feedback").removeClass('glyphicon-ok')   
    return false 
  }

  if($("#password1").val() == $("#password2").val()) {
      $("#pw2_div").toggleClass('has-error', false)
      $("#pw2_div").toggleClass('has-success', true)
      $("#submit").prop('disabled', false)
      $("#pw2_feedback").addClass('glyphicon-ok')
      $("#pw2_feedback").removeClass('glyphicon-remove')
      document.getElementById("pw2_comments").innerText = ""
      document.getElementById("warning").style.display = "none"
      return true
  } else {
      $("#pw2_div").toggleClass('has-error', true)
      $("#pw2_div").toggleClass('has-success', false)
      $("#submit").prop('disabled', true)
      $("#pw2_feedback").addClass('glyphicon-remove')
      $("#pw2_feedback").removeClass('glyphicon-ok')
      document.getElementById("pw2_comments").innerText = "passwords do not match";
      return false;
  }
}

function checkEmail(email) {
    // if (email.length == 0) { 
    //   $("#email_div").toggleClass('has-success', false);
    //   return false;
    // }

    re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    // regex is a variation of the official standard: RFC 5322
    // see http://www.regular-expressions.info/email.html
    // re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b/

    matches = email.search(re)
    if (matches < 0) {
      document.getElementById("email_comments").innerText = "incorrect e-mail format";
      $("#email_div").toggleClass('has-error', true);
      $("#email_div").toggleClass('has-success', false);
      $("#submit").prop('disabled', true)
      $("#email_feedback").addClass('glyphicon-remove')
      $("#email_feedback").removeClass('glyphicon-ok')
    } else {
      document.getElementById("email_comments").innerText = "";
      $("#email_div").toggleClass('has-error', false);
      $("#email_div").toggleClass('has-success', true);   
      $("#submit").prop('disabled', false)
      $("#email_feedback").addClass('glyphicon-ok')
      $("#email_feedback").removeClass('glyphicon-remove')
      document.getElementById("warning").style.display = "none"
    }
}

function validateForm() {
    if( $("#user_div" ).hasClass( "has-success" ) && $("#pw1_div").hasClass("has-success") && $("$pw2_div").hasClass("has-success") && $("#email_div").hasClass("has-success") && ($("#password1").val() == $("#password2").val())) {
        return true;
    } else {
        document.getElementById("warning").innerHTML = "ERROR: correct blanks and/or errors and try again";
        document.getElementById("warning").style.display = "block"
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
    /*width: 200px;*/
  }
</style>

<body>

<div class="container">
  <div class="main left">
      <h2 align="center">Registration</h2>
      <div style="height:10px"></div>

      <form class="form-horizontal" name="reg_form" action="/register" method="post" onsubmit="return validateForm()">

        <div id="user_div" class="form-group has-feedback">
          <label for="username" class="control-label col-xs-12 col-sm-offset-2 col-sm-2">Username:</label>
          <div class="col-xs-12 col-sm-4">
            <input class="form-control" id="user" type="text" name="user" onkeyup="fixUsername(this.value)" onchange="checkUser(this.value)">
            <span id="user_feedback" style="right:20px" class="glyphicon form-control-feedback"></span>
            <span id="user_comments" class="text-danger"></span>
          </div>
        </div>

        <div id="pw1_div" class="form-group has-feedback">
          <label for="password1" class="control-label col-xs-12 col-sm-offset-2 col-sm-2">Password:</label>
          <div class="col-xs-12 col-sm-4">
            <input class="form-control" type="password" name="password1" id="password1" onkeyup="checkPassword(this.value)">
            <span id="pw1_feedback" style="right:20px" class="glyphicon form-control-feedback"></span>
            <span id="pw1_comments" class="text-danger"></span>
          </div>
        </div>

        <div id="pw2_div" class="form-group has-feedback">
          <label for="password2" class="control-label col-xs-12 col-sm-offset-1 col-sm-3">Retype Password:</label>
          <div class="col-xs-12 col-sm-4">
            <input class="form-control" type="password" name="password2" id="password2" onkeyup="checkPasswordMatch()" onblur="checkPasswordMatch()">
            <span id="pw2_feedback" style="right:20px" class="glyphicon form-control-feedback"></span>
            <span id="pw2_comments" class="text-danger"></span>
          </div>
        </div>

        <div id="email_div" class="form-group has-feedback">
          <label for="email" class="control-label col-xs-12 col-sm-offset-2 col-sm-2">Email:</label>
          <div class="col-xs-12 col-sm-4">
            <input class="form-control" type="text" name="email" id="email" onkeyup="checkEmail(this.value)">
            <span id="email_feedback" style="right:20px" class="glyphicon form-control-feedback"></span>
            <span id="email_comments" class="text-danger"></span>
          </div>
        </div>

        <div id="warning" align="center" style="display:none; border:1px solid #A94442" class="alert-danger col-xs-12 col-sm-offset-2 col-sm-8"></div><br><br>

        <input class="btn btn-primary col-xs-12 col-sm-offset-5 col-sm-2" style="align:center" type="submit" id="submit" value="Register" class="btn">

      </form>
  </div>

  <br><br>
  <hr>
    <p align="center">Already have an account?
    <a class="btn btn-link" href="/login">Login</a></p>

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
