%include("header")

<div class="container-fluid">
<h3>Configure inputs: step 2 of 3</h3><br>

<h4>Parse input file</h4>

<p>Choose how to parse this file:</p>

<form method="post" action="/appconfig/inputs/create_view">
    %include('appconfig/input_opts')
    <br>
    <input type="hidden" name="appname" value="{{appname}}">
    <input type="submit" class="btn btn-primary" value="Parse">
</form>

<hr>

<pre>
{{!contents}}
</pre>
</div>

%include('footer')
