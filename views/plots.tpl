%include header title='Available Plots'
%include navbar

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

<style type="text/css">
td {text-align: center}
</style>

<!--<h1>{{app}}</h1>-->

<h2 align=center>Available plots for {{cid}}</h2>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<table border="1" cellpadding=10 align=center>
<tr bgcolor="dfdfdf" > <th>Title</th> <th>Type</th> <th>Filename</th> <th>X-Column</th> <th>Y-Column</th> <th>Action</th> </tr>
%for row in rows:
  <tr>
  <td>{{row[5]}}</td>
  <td>{{row[1]}}</td>
  <td>{{row[2]}}</td>
  <td>{{row[3]}}</td>
  <td>{{row[4]}}</td>
  <td><a href="/{{app}}/{{cid}}/plot/{{row[0]}}">plot</a> -
      <a href="/{{app}}/plots/delete/{{row[0]}}">delete</a> 
  <!--
  <form method="get" action="/apps/delete/{{row[0]}}">
     <td><input type="button" value="delete"></td> 
  </form>
  -->
</tr> 
%end
</table>

<h2>Add a new plot to: {{app}}</h2>

<form method="post" action="/{{app}}/plots/create">
   Filename to plot (use <cid> to use the case id): <input type="text" name="fn"><br>
   Title: <input type="text" name="title"><br>
   X-Column: <input type="text" name="col1"><br>
   Y-Column: <input type="text" name="col2"><br>
   Type of plot:
   <select name="ptype">
       <option VALUE="line">line</option>
       <option VALUE="scatter">scatter</option>
       <option VALUE="bar">bar</option>
   </select><br>
   <input type="submit">
</form>

%include footer
