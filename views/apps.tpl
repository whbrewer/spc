%include header title='Installed Apps'

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

<center>
<a href="/"><img src="/static/images/scipaas.png" width="50%"></a>
<p><font size="+2"><i>a scientific platform-as-a-service</i></font></p>
</center>

<p>
<font size="+1">
<a href="/apps/add"><img src="/static/images/plus.png" align=left valign=bottom></a>
SciPaaS is a middleware execution platform
for easily uploading and running scientific apps in the cloud.</p>
</font>

<h1>Installed Apps</h1>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<table border="1">
<tr> <th><a href="/apps/show/name">Name</a></th> <th>Description</th> <th><a href="/apps/show/category">Category</a></th> <th><a href="/apps/show/language">Language</a></th> <th>Delete</th> </tr>
%for row in rows:
  <tr>
  <td><a href="/{{row[1]}}">{{row[1]}}</a></td>
  <td>{{row[2]}}</td>
  <td>{{row[3]}}</td>
  <td>{{row[4]}}</td>
  <td><a href="/apps/delete/{{row[0]}}">delete</a></td>
  <td><a href="/apps/edit/{{row[0]}}">edit</a></td>
  <!--
  <form method="get" action="/apps/delete/{{row[0]}}">
     <td><input type="button" value="delete"></td> 
  </form>
  -->
</tr> 
%end
</table>
