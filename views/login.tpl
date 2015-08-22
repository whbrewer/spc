%include('header')

<body>

<div class="main left">
    <h1>Sign in</h1>
    <form class="form-horizontal" action="/login" method="post">
        <div class="form-group">
            <label for="username" class="control-label col-md-3">Username:</label>
            <div class="col-md-6">
                <div class="input-group" style="width:200px">
                    <div class="input-group-addon">
                        <span class="glyphicon glyphicon-user"></span>
                    </div>
                    <input type="text" class="form-control" name="user" id="user" />
                </div>
            </div>
        </div>
        <div class="form-group">
            <label for="password" class="control-label col-md-3">Password:</label>
            <div class="col-md-6">
                <div class="input-group" style="width:200px">
                    <div class="input-group-addon">
                       <span class="glyphicon glyphicon-lock"></span>
                    </div>
                    <input type="password" class="form-control" name="passwd" id="passwd" />
                </div>
            </div>
        </div>

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
