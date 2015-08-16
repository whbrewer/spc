%include('header')

<body>

<div class="main left">
    <h1>Sign in</h1>
    <form action="/login" method="post">
        Username:<br>
        <input class="form-control" type="text" style="width:200px" name="user"><br>
        Password:<br>
        <input class="form-control" type="password" style="width:200px" name="passwd"><br>
        <!--<a href="/forgot">Forgot your password?</a><br>-->
        <a href="/register">Register for an account</a><br>
        <!--<input type="checkbox" name="ssi"> Stay signed in<br>-->
        <input type="hidden" name="referrer" value="{{referrer}}">
        <div class="col-xs-12" style="height:5px"></div>
        <input class="btn btn-primary" type="submit" value="Sign in" class="btn"><br><br>
    </form>
</div>

</body>
</html>
