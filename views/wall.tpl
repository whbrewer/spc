%include header title='Wall'

<body onload="init()">
%include navbar

<h2 align=center>Wall</h2>

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr> 
   <th>id</th> 
   <th>user</th> 
   <th>app</th> 
   <th>cid</th> 
   <th>comment</th> 
</tr>
</thead>

%for row in rows:
  <tr>
  <td>{{row[0]}}</td>
  <td>{{row[1]}}</td>
  <td>{{row[2]}}</td>
  <td>{{row[3]}}</td>
  <td>{{row[4]}}</td>
  </tr> 
%end
</table>

%include footer
