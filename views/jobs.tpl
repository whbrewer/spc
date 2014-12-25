%include header title='Job scheduler'

<body onload="init()">
%include navbar

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
  <td>{{row[0]}}</td>
  <td>{{row[2]}}</td>
  <td>{{row[3]}}</td>
  <td>{{row[4]}}</td>
  <td>{{row[5]}}</td>

  <td><a href="/jobs/delete/{{row[0]}}">delete</a> ::
      <a href="/{{row[2]}}/{{row[3]}}/monitor">monitor</a> :: 
      <a style="cursor: pointer" onclick="set_cid('{{row[3]}}','{{row[2]}}')"><u>set</u></a><br><br>
      <form method="post" action="/wall">
      <input type="hidden" name="app" value="{{app}}">
      <input type="hidden" name="jid" value="{{row[0]}}">
      <input type="text" name="comment">
      <input type="submit" value="Post to wall"></a></form></td>
</tr> 
%end
</table>

%include footer
