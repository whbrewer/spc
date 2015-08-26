<!DOCTYPE html>
<html>
<head>
<link rel="Stylesheet" href="/static/css/bootstrap.min.css" />
</head>
<body>

<div class="container-fluid">
<h3>Configure inputs: step 2 of 3</h3><br>

<h4>Parse input file</h4>

<p>Choose how to parse this file:</p>

<form method="post" action="/inputs/edit/create_view">
    <select class="form-control" style="width:auto" name="input_format">
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
    </select><br>
    
    <input type="hidden" name="appname" value="{{appname}}">
    <input type="submit" class="btn btn-primary" value="Parse">
</form>

<hr>

<pre>
{{!contents}}
</pre>
</div>

%include('footer')
