%style = ".table { font-size: 120% }"
%rebase('base.tpl', style=style)

<h1 class="text-center">Users</h1>

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
              <input type="hidden" name="del_files" value="True">
              <button class="btn btn-link" style="color:#d9302c; font-size:150%" type="submit">
                <span class="glyphicon glyphicon-remove-sign"></span>
              </button>
          </form>
          <!-- <input class="btn btn-danger" type="submit" value="delete"></form> -->
      </td>
  </tr>
%end
</tbody>
</table>
