<!DOCTYPE html>
<html>
<head>
<link rel="Stylesheet" href="/static/bootstrap/css/bootstrap.min.css" />
</head>
<body>

<div class="container-fluid">
<h1>Step 3</h1>
<h2>parse input file</h2>
<p>choose how to parse this file:</p>


<form method="post" action="/addapp/step4">
    <select name="input_format">
        %opts = {'namelist':'namelist.input','ini':'INI file','xml':'XML file'}
        %for key, value in opts.iteritems():
            %if key == input_format:
                <option selected value="{{key}}">{{value}}
            %else:
                <option value="{{key}}">{{value}}
            %end
        %end
        <!--<option value="namelist">namelist.input
        <option value="ini">INI file
        <option value="xml">xml file-->
    </select>
    <input type="hidden" name="appname" value="{{appname}}">
    <input type="submit" class="btn btn-primary" value="Parse">
</form>

<hr>

<pre>
{{!contents}}
</pre>
</div>

%include('footer')
