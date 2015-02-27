%include('header')
%include('navbar')
%include('navactions')

<h1>{{fn}}</h1>

<fieldset>
<legend>Actions</legend>
<a href="/monitor?cid={{cid}}&app={{app}}">monitor</a> :: 
<a href="/files?cid={{cid}}&app={{app}}">files</a> :: 
<a href="/zipcase?cid={{cid}}&app={{app}}">zipcase</a> :: 
<a href="/start?cid={{cid}}&app={{app}}">start</a> :: 
<a href="/jobs/delete/{{id}}?cid={{cid}}&app={{app}}">delete</a> 
<br><br>
<form method="post" action="/wall">
      <input type="hidden" name="app" value="{{app}}">
      <input type="hidden" name="cid" value="{{cid}}">
      <input type="hidden" name="jid" value="{{jid}}">
      <input type="text" name="comment">
      <input type="submit" value="Post to wall">
</form>
</fieldset>

<pre>
{{!contents}}
</pre>

%include('footer')
