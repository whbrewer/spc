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
<th>Name</th> 
<th>Description</th> 
<th>Category</th> 
<th>Language</th> 
<th>Command Line Options</th>
</tr>
</thead>

%for row in rows:
  <tr>
  <td><a href="/{{row['name']}}">{{row['name']}}</a></td>
  <td>{{row['description']}}</td>
  <td>{{row['input_format']}}</td>
  <td>{{row['language']}}</td>
  <td>{{row['cmd_line_opts']}}</td>
<!--
  <form method="post" action="/apps/delete/{row[0]}}">
     <td><input type="button" value="delete"></td> 
  </form>
-->
</tr> 
%end
</table>
<a href="/apps/add"><img src="/static/images/plus.png" align=left valign=bottom>Add an app</a>

%include footer
