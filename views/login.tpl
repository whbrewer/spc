<link rel="Stylesheet" type="text/css" href="/static/css/login.css" />

<body>

<div class="main left">
    <h1>Sign in</h1>
    <form action="/login" method="post">
        Username:<br>
        <input type="text" name="user"><br>
        Password:<br>
        <input type="password" name="passwd"><br>
        <!--<a href="/forgot">Forgot your password?</a><br>-->
        <a href="/register">Register for an account</a><br>
        <!--<input type="checkbox" name="ssi"> Stay signed in<br>-->
        <input type="hidden" name="referrer" value="{{referrer}}">
        <input type="submit" value="Sign in" class="btn"><br><br>
    </form>
</div>

</body>
</html>
