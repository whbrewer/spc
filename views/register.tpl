%include('header')

<script>
function checkUser(user) {
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
            $("#submit").prop('disabled',true)
            alert("Username " + user + " is taken.\nPlease use another name.");
         } else {
            document.reg_form.password1.focus()
            $("#user_div").toggleClass('has-error', false);
            $("#user_div").toggleClass('has-success', true);
            $("#submit").prop('disabled',false)
         }
      }
   })
}

function checkPassword(pw) {
  var msg = "";
  var nerrors = 0;

  if (pw.length < 8) {
    msg += "ERROR: password must be at least 8 characters.  ";
    nerrors += 1;  
  }

  if (pw === pw.toLowerCase()) {
    msg += "ERROR: password doesn't contain any uppercase characters";
    nerrors += 1;
  }

  if (pw.search(/[0-9]/) < 0) {
    msg += "ERROR: password must have at least one digit";
    nerrors += 1;
  }

  if (nerrors > 0) {
    $("#pw1_div").toggleClass('has-error', true);
    $("#pw1_div").toggleClass('has-success', false);
  } else {
    $("#pw1_div").toggleClass('has-error', false);
    $("#pw1_div").toggleClass('has-success', true);
  }

  document.getElementById("warning").innerText = msg;
}

function checkPasswordMatch(pw) {
    if($("#password1").val() == $("#password2").val()) {
        document.getElementById("warning").innerText = "";
        $("#pw2_div").toggleClass('has-error', false);
        $("#pw2_div").toggleClass('has-success', true); 
    } else {
        document.getElementById("warning").innerText = "ERROR: passwords do not match";
        $("#pw2_div").toggleClass('has-error', true);
        $("#pw2_div").toggleClass('has-success', false);
        return false;
    }
}

function checkEmail(email) {
    // regex is a variation of the official standard: RFC 5322
    // see http://www.regular-expressions.info/email.html
    re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b/
    //'
    matches = email.search(re)
    if (matches < 0) {
      //alert("please enter a valid email")
      document.getElementById("warning").innerText = "ERROR: password must be at least 8 characters";
      $("#email_div").toggleClass('has-error', true);
      $("#email_div").toggleClass('has-success', false);
    } else {
      document.getElementById("warning").innerText = "";
      $("#email_div").toggleClass('has-error', false);
      $("#email_div").toggleClass('has-success', true);   
    }
}

function validateForm() {
    if($("#password1").val() == $("#password2").val()) {
        return true;
    } else {
        alert("passwords do not match")
        return false;
    }
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
        <div class="col-md-6">
          <input class="form-control" type="text" name="user" id="user" onchange="checkUser(this.value)">
        </div>
      </div>

      <div id="pw1_div" class="form-group">
        <label for="password1" class="control-label col-md-3">Password:</label>
        <div class="col-md-6">
          <input class="form-control" type="password" name="password1" id="password1" onchange="checkPassword(this.value)">
        </div>
      </div>

      <div id="pw2_div" class="form-group">
        <label for="password2" class="control-label col-md-3">Retype Password:</label>
        <div class="col-md-6">
          <input class="form-control" type="password" name="password2" id="password2" onchange="checkPasswordMatch(this.value)">
        </div>
      </div>

      <div id="email_div" class="form-group">
        <label for="email" class="control-label col-md-3">Email:</label>
        <div class="col-md-6">
          <input class="form-control" type="text" name="email" id="email" onchange="checkEmail(this.value)">
        </div>
      </div>

      <input class="btn btn-primary" type="submit" id="submit" value="Register" class="btn">
    </form>
</div>

</body>
</html>
