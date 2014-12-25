%include('header')
%include('navbar')

<body onload="init()">
<script>
function delete(id) {
   if(!confirm("Are you sure to delete?")) return                      
      document.student_modify.action = "/apps/delete/id"
      document.student_modify.submit()
   }
}
function edit(id) {
   if(!confirm("Are you sure to delete?")) return                      
      document.student_modify.action = "/apps/delete/id"
      document.student_modify.submit()
   }
}
</script>

<h1>Installed Apps</h1>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr> 
<th><a href="/apps/show/name">Name</a></th> 
<th>Description</th> 
<th><a href="/apps/show/category">Category</a></th> 
<th><a href="/apps/show/language">Language</a></th> 
<th>Delete</th> 
</tr>
</thead>

%for row in rows:
  <tr>
  <td><a href="/{{row[1]}}">{{row[1]}}</a></td>
  <td>{{row[2]}}</td>
  <td>{{row[3]}}</td>
  <td>{{row[4]}}</td>
  <td><a href="/apps/delete/{{row[0]}}">delete</a></td>
  <!--
  <form method="get" action="/apps/delete/{{row[0]}}">
     <td><input type="button" value="delete"></td> 
  </form>
  -->
</tr> 
%end
</table>
<a href="/apps/add"><img src="/static/images/plus.png" align=left valign=bottom>Add an app</a>

%include footer
