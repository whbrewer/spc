<!DOCTYPE html>
<html>
<head>
<link rel="Stylesheet" href="/static/bootstrap/css/bootstrap.min.css" />
<script src="/static/js/flot/jquery.js"></script>
<script>
function checkApp(appname) {
   jQuery.ajax({
      type: "POST",
      url:  "/app_exists/"+appname,
      data: { appname: appname },
      complete: function(xhr){
         var response = eval(xhr.responseText);
         if (response) {
            $("#appname").css("background-color","#D3ABAE")
            $("#appname").select()
            $("#submit").prop('disabled',true)
            alert("Appname " + appname + " is taken.\nPlease try another name.");
         } else {
            $("#appname").css("background-color","#86C98A")
            $("#submit").prop('disabled',false)
         }
      }
   })
}
</script>
</head>
<body>

<div class="container-fluid">
    <h1>Add new app to SciPaaS</h1>
    <form action="/addapp/step1" method="post">
        <h2>Enter name of app:</h2>
        <input type="text" id="appname" name="appname" 
               onchange="checkApp(this.value)"><br>
        <input type="submit" class="btn btn-primary" id="submit" value="Next >>"><br><br>
    </form>
</div>

%include('footer')

