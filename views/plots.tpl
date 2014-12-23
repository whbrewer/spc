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

<h2 align=center>Available plots for {{app}} app ({{cid}})</h2>

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
  <td><a href="/plot/{{row[0]}}?app={{app}}&cid={{cid}}"><img src="/static/plot.png"></a> -
      <a href="/plots/delete/{{row[0]}}?app={{app}}&cid={{cid}}">delete</a> 
  <!--
  <form method="get" action="/apps/delete/{{row[0]}}">
     <td><input type="button" value="delete"></td> 
  </form>
  -->
</tr> 
%end
</table>

<hr>
<h2>Add a new plot to {{app}} app</h2>

<form method="post" action="/plots/create">
   Filename to plot (use <cid> to use the case id): <input type="text" name="fn"><br>
   Title: <input type="text" name="title"><br>
   X-Column: 
   <select name="col1">
       <option value="1">1</option>
       <option value="2">2</option>
       <option value="3">3</option>
       <option value="4">4</option>
       <option value="5">5</option>
       <option value="6">6</option>
       <option value="7">7</option>
       <option value="8">8</option>
       <option value="9">9</option>
   </select><br>

   Y-Column:
   <select name="col2">
       <option value="1">1</option>
       <option value="2">2</option>
       <option value="3">3</option>
       <option value="4">4</option>
       <option value="5">5</option>
       <option value="6">6</option>
       <option value="7">7</option>
       <option value="8">8</option>
       <option value="9">9</option>
   </select><br>

   <!-- <input type="text" name="col1"><br> -->
   <!-- <input type="text" name="col2"><br> -->
   Type of plot:
   <select name="ptype">
       <option VALUE="line">line</option>
       <option VALUE="categories">categories (bar plot)</option>
   </select><br>
   <input type="hidden" name="app" value="{{app}}">
   <input type="hidden" name="cid" value="{{cid}}">
   <input type="submit">
</form>

%include footer
