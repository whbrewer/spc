%rebase('base.tpl')

<h3>Configure Executable: step 2 of 2</h3><br>

<h4>Success!</h4>

<!-- <p>Choose test type:</p>

<form method="post" action="/appconfig/exe/test">
    <select class="form-control" style="width:auto" name="input_format">
        <option value="ldd">LDD
    </select><br>
    <input type="hidden" name="appname" value="{{appname}}">
    <input type="submit" class="btn btn-primary" value="Test">
</form> -->

<font size="+1">
<p>Redirecting to <a href="/app/{{appname}}">app configuration page</a></p>

<meta http-equiv="refresh" content="1; url=/app/{{appname}}">
</font>

<!-- <font size="+1">
<a href="/apps">Browse Apps</a><br>
<a href="/app/{{appname}}">Edit {{appname}}</a><br>
<a href="/{{appname}}">Test {{appname}}</a>
</font>
 -->

<hr>

<pre>
{{!contents}}
</pre>
</div>
