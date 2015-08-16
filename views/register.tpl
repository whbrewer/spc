%include('header')

<!-- <link rel="stylesheet" href="/static/css/login.css" /> -->
<link rel="stylesheet" href="/static/css/strength.css" />
<script src="/static/js/strength.js"></script>

<script>
function checkUser(user) {
   jQuery.ajax({
      type: "POST",
      url:  "/check_user", 
      data: { user: user },
      complete: function(xhr){
         var response = eval(xhr.responseText);
         if (response) {
            $("#user").css("background-color","#D3ABAE")
            $("#user").select()
            $("#submit").prop('disabled',true)
            alert("Username " + user + " is taken.\nPlease use another name.");
         } else {
            document.reg_form.password1.focus()
            $("#user").css("background-color","#86C98A")
            $("#submit").prop('disabled',false)
         }
      }
   })
}

function checkEmail(email) {
    // regex is a variation of the official standard: RFC 5322
    // see http://www.regular-expressions.info/email.html
    re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b/
    matches = email.search(re)
    if (matches < 0) {
        alert("please enter a valid email")
        
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

<body>

<div class="main left">
    <h1>Register</h1>
    <form name="reg_form" action="/register" method="post" onsubmit="return validateForm()">
        <input class="form-control" placeholder="username" type="text" name="user" id="user" onchange="checkUser(this.value)" style="width:200px"><br>
        <input class="form-control" placeholder="password" type="password" name="password1" id="password1" style="width:200px"><br><br>
        <input class="form-control" placeholder="password (again)" type="password" name="password2" id="password2" style="width:200px"><br>
        <input class="form-control" placeholder="email address" type="text" name="email" id="email" onchange="checkEmail(this.value)" style="width:200px"><br>
        <input class="btn btn-primary" type="submit" id="submit" value="Register" class="btn"><br><br>
    </form>
</div>

<script>
  $(document).ready(function ($) { $('#password1').strength(); });
</script>

</body>
</html>
