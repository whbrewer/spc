%include('header')
%include('navbar')

<body onload="init()">
<script>
//function delete(id) {
//   if(!confirm("Are you sure to delete?")) return                      
//      document.student_modify.action = "/apps/delete/id"
//      document.student_modify.submit()
//   }
//}
//function edit(id) {
//   if(!confirm("Are you sure to delete?")) return                      
//      document.student_modify.action = "/apps/delete/id"
//      document.student_modify.submit()
//   }
//}
//function load_plot(fn) {
//   $("#fn").val(fn)
//}
</script>

<style type="text/css">
td {text-align: center}
</style>

<!--<h1>{{app}}</h1>-->

<h1 align=center>Available plots for {{app}} app</h1>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr>
   <th>Title</th> 
   <th>Type</th> 
   <th>Options</th> 
   <th>Data Definition</th> 
   <th>Action</th> 
</tr>
</thead>
%for row in rows:
  <tr>
     <td>{{row['plots']['title']}}</td>
     <td width="50">{{row['plots']['ptype']}}</td>
     <td>{{row['plots']['options']}}</td>
     <td>{{row['plots']['datadef']}}</td>
  <td width="100"><a href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">plot</a> <br>
      <a href="/plots/delete/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">delete</a> <br>
      <a href="/plots/datasource/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">datasource</a></td>

  <!--
  <form method="get" action="/apps/delete/{row[0]}}">
     <td><input type="button" value="delete"></td> 
  </form>
  -->
</tr> 
%end
</table>

<h1>Add a new plot to {{app}} app</h1>

<form method="post" action="/plots/create">
<table padding=10>
   <tr><td>Filename to plot:</td>
       <td><input id="fn" type="text" name="fn"></td>
       <td><em>Note: use &lt;cid&gt; to use the case id</em></td></tr>
   <tr><td>Title:</td> <td><input type="text" name="title"></td></tr>
   <tr><td>Type of plot:</td>
   <td><select name="ptype">
       <option VALUE="flot-line">flot/line</option>
       <option VALUE="flot-cat">flot/categories</option>
       <option VALUE="flot-bar">flot/bar</option>
       <option VALUE="mpl-line">matplotlib/line</option>
       <option VALUE="mpl-bar">matplotlib/bar</option>
   </select></td></tr>
   <tr><td>options:</td> <td><textarea name="options"></textarea></td></tr>
   <tr><td>data definition:</td> <td><textarea name="datadef"></textarea></td></tr>
   <tr><td></td><td><input type="submit"></td></tr>
   <input type="hidden" name="app" value="{{app}}">
   <input type="hidden" name="cid" value="{{cid}}">
</table>
</form>

%include('footer')
