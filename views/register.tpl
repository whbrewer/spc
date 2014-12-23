<link rel="Stylesheet" type="text/css" href="/static/css/login.css" />
<script src="/static/flot/jquery.js"></script>
<script src="/static/register.js"></script>

<script>
function checkUser(user) {
   jQuery.ajax({
      type: "POST",
      url:  "/check_user", 
      data: { user: user },
      complete: function(xhr){
         var response = eval(xhr.responseText);
         if (response) {
            alert("Username " + user + " is taken.\nPlease use another name.");
            $("#user").css("background-color","#D3ABAE")
            $("#user").select()
            //$("#user").val('')
         } else {
            document.reg_form.password1.focus()
            $("#user").css("background-color","#86C98A")
         }
      }
   })
}
</script>

<body>

<div class="main left">
    <h1>Register</h1>
    <form name="reg_form" action="/register" method="post">
        Email/Username<br>
        <input type="text" name="user" id="user" onchange="checkUser(this.value)"><br>
        Password<br>
        <input type="password" name="password1" id="password1"><br>
        <input type="password" name="password2" id="password2"><br>
        <input type="submit" value="Register" class="btn"><br><br>
    </form>
</div>

</body>
</html>
