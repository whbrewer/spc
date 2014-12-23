%include header title='Job scheduler'
<!--<meta http-equiv="refresh" content="5">-->

<body onload="init()">
%include navbar

<table border="1">
<tr> <th>jid</th> <th>user</th> <th>app</th> <th>cid</th> <th>comment</th> </tr>
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
