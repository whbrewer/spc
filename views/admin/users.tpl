%include('header')

<body onload="init()">

<style>
  .table {
    font-size: 120%;
  }
</style>

%include('navbar')
<h1 align=center>Users</h1>

<table class="table table-striped">
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
          <input class="btn btn-default" type="submit" value="delete"></form></td>
  </tr> 
%end
</tbody>
</table>

%include('footer')
