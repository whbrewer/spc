%include('header')
%include('navbar')

%if defined('status'):
    Status: {{status}}
%end

<div class="container-fluid">
    <div class="col-md-offset-4">
        <font size="+2">case: {{cid}}</font>
        <div class="btn-group">
            <form class="btn-group" method="get" action="/start?cid={{cid}}&app={{app}}">
                <input type="submit" class="btn btn-default" value="restart">
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>
            <form class="btn-group" method="get" action="/files?cid={{cid}}&app={{app}}">
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
                <input type="submit" class="btn btn-default" value="files">
            </form>
            <form class="btn-group" method="post" action="/shared/unshare">
                <input type="hidden" name="app" value="{{app}}">
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="jid" value="{{jid}}">
                <input type="submit" class="btn btn-default" value="unstar">
            </form>
        </div>
    </div>
</div>

<!--
<table id="clickable">
<tr> <td>post id:</td>  <td>{{sid}}</td> </tr>
<tr> <td>case id:</td>  <td>{{cid}}</td> </tr>
<tr> <td>owner:</td>  <td>{{user}}</td> </tr>
</table>
-->

<pre>
{{!contents}}
</pre>
<span>file is: {{fn}}</span>

%include('footer')
