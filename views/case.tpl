%include('header')
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
<form method="get" action="/zipcase?cid={{cid}}&app={{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
    <input type="hidden" name="app" value="{{app}}">
    <input type="submit" value="zip case">
</form>
</td> <td>
<form method="post" action="/jobs/delete/{{jid}}">
    <input type="hidden" name="cid" value="{{cid}}">
    <input type="hidden" name="app" value="{{app}}">
    <input type="submit" value="delete" 
           onclick="if(confirm('are you sure?')) return true; return false">
</form>
</td><td>
<form method="post" action="/shared">
      <input type="hidden" name="app" value="{{app}}">
      <input type="hidden" name="cid" value="{{cid}}">
      <input type="hidden" name="jid" value="{{jid}}">
      <input type="text" name="comment">
      <input type="submit" value="Share">
</form>
</td></tr>
</table>
</fieldset>

<!--
<form>
<select id="selector" onchange="show(this.value)">
<option value="Show output every...">
<option value="500">500ms
<option value="1000">1s
<option value="5000">5s
<option value="10000">10s
<option value="30000">30s
<option value="60000">1m
<option value="10000000000">&infin;
</select>
</form>
-->

<div id="output" style="width:648px;height:200px;"></div>

<script>
function show(update_interval) {
    showOutput = function() {
       jQuery('#output').load('/{{app}}/{{cid}}/tail', function(){
          setTimeout(showOutput, update_interval);
       })
    }
    //$("#selector").hide()
    showOutput();
}
show(1000);
</script>

%include('footer')
