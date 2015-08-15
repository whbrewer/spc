<!DOCTYPE html>
<html>
<head>
<link rel="Stylesheet" href="/static/css/bootstrap.min.css" />
</head>

<body>

<div class="container-fluid">
<h1>Step 4</h1>

<h2>parsed inputs &ndash; assign html input types</h2>

<form method="post" action="/addapp/step5">
<input type="submit" class="btn btn-primary" value="Next >>">
<hr>
How to represent a true Boolean value (e.g. T, True, true, 1)?
<input class="form-control" type="text" style="width:100px" name="bool_rep">
<hr>
<table class="table table-striped">
<thead align=left>
    <th>parameter</th>
    <th>value</th>
    <th>html_tag_type</th>
    <th>description</th>
    <!--<th>data_type</th>-->
</thead>
<tbody>
%for key,value in inputs.iteritems():
    <tr>
        <td>{{key}}</td> <td>{{value}}</td> 
        <td><select class="form-control" name="html_tags">
            <option value="text">text
            <option value="hidden">hidden
            <option value="select">select
            <option value="checkbox">checkbox
        </select></td>
        <!--
        <td><select name="data_type">
            <option value="string">String
            <option value="integer">Integer
            <option value="float">Float
            <option value="boolean">Boolean
        </select></td>
        -->
        <td><input class="form-control" type="text" name="descriptions" value="{{key}}"></td>
    </tr>
    <input type="hidden" name="keys" value="{{key}}">
    <input type="hidden" name="appname" value="{{appname}}">
    <input type="hidden" name="input_format" value="{{input_format}}">
%end
</tbody>
</table>
</form>

<hr>
</div>

%include('footer')

