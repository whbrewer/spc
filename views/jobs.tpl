%include('header')

<body onload="init()">
%include('navbar')

<h1 align=center>{{user}}'s jobs</h1>

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr>
  <th>jid</th> 
  <th>app</th> 
  <th>cid</th> 
  <th>state</th> 
  <th>time_submit</th> 
  <th>actions</th>
</tr>
</thead>

%for row in rows:
  <tr>
  <td>{{row['id']}}</td>
  <td>{{row['app']}}</td>
  <td>{{row['cid']}}</td>
  <td>{{row['state']}}</td>
  <td>{{row['time_submit']}}</td>
  <td><a href="/jobs/delete/{{row['id']}}">delete</a> ::
      <a href="/{{row['app']}}/{{row['cid']}}/monitor">monitor</a> :: 
      <a href="/jobs/stop/{{row['app']}}">stop</a> ::
      <a style="cursor: pointer" onclick="set_cid('{{row['cid']}}','{{row['app']}}')"><u>set</u></a><br><br>
      <form method="post" action="/wall">
      <input type="hidden" name="app" value="{{app}}">
      <input type="hidden" name="jid" value="{{row['id']}}">
      <input type="text" name="comment">
      <input type="submit" value="Post to wall"></a></form></td>
</tr> 
%end
</table>

%include footer
