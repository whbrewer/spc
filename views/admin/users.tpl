%include('header')

<body onload="init()">
%include('navbar')
%include('tablesorter')
<h1 align=center>Users</h1>

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr>
  <th>user</th> 
  <th>email</th> 
  <th>actions</th>
</tr>
</thead>
<tbody>
%for row in rows:
  <tr>
     <td>{{row['user']}}</td>
     <td>{{row['email']}}</td>
     <td> <form method="post" action="/admin/delete_user" 
                onclick="if(confirm('confirm')) return true; return false">
          <input type="hidden" name="uid" value="{{row['id']}}">
          <input type="submit" value="delete"></form></td>
  </tr> 
%end
</tbody>
</table>

%include('footer')
