%include('header')
<link type="text/css" rel="StyleSheet" href="/static/css/clickable_rows.css"/>

%include('navbar')
%include('navactions')

<fieldset>
<legend>Actions</legend>
%if defined('status'):
    Status: {{status}}
%end

<table>
<tr>
<td>
<form method="get" action="/start?cid={{cid}}&app={{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
    <input type="hidden" name="app" value="{{app}}">
    <input type="submit" value="start">
</form>
</td> <td>
<form method="get" action="/files?cid={{cid}}&app={{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
    <input type="hidden" name="app" value="{{app}}">
    <input type="submit" value="files">
</form>
</td> <td>
<form method="post" action="/shared/delete">
    <input type="hidden" name="cid" value="{{cid}}">
    <input type="hidden" name="app" value="{{app}}">
    <input type="hidden" name="sid" value="{{sid}}">
    <input type="submit" value="delete comment" 
           onclick="if(confirm('are you sure?')) return true; return false">
</form>
</td>
</tr>
</table>
</fieldset>

<!--
<table id="clickable">
<tr> <td>post id:</td>  <td>{{sid}}</td> </tr>
<tr> <td>case id:</td>  <td>{{cid}}</td> </tr>
<tr> <td>owner:</td>  <td>{{user}}</td> </tr>
</table>
-->

<h1>{{fn}}</h1>
<pre>
{{!contents}}
</pre>

%include('footer')
