%include('header')
<body>
%include('navbar')

<div class="container-fluid">
<div class="col-xs-12" style="height:5px"></div>

<div align="center" class="alert-info">
    <em>Wrote parameters to input file. Click Execute to start simulation.</em>
</div>

<form action="/execute" method="post">
    <input type="hidden" name="np" value="1">

    <div class="col-xs-12" style="height:5px"></div>
    <button type="submit" class="btn btn-success"> <!-- pull-right -->
        Execute <em class="glyphicon glyphicon-play"></em>
    </button>

    <div class="col-xs-12" style="height:5px"></div>

    <input type="hidden" name="app" value="{{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
    %if defined('desc'):
    	<input type="hidden" name="desc" value="{{desc}}">
    %else:
    	<input type="hidden" name="desc" value="None">
    %end

<pre>
<!-- don't indent the following -->
{{!inputs}}
</pre>

</form>

</div>

%include('footer')
