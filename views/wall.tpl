%include header title='Job scheduler'
<!--<meta http-equiv="refresh" content="5">-->

<body onload="init()">
%include navbar

<table border="0">
<tr> <th>jid</th> <th>user</th> <th>app</th> <th>cid</th> <th>state</th> <th>time_submit</th> <th>description</th> </tr>
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
</tr> 
%end
</table>

%include footer
