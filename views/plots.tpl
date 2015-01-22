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

<style type="text/css">
td {text-align: center}
</style>

<!--<h1>{{app}}</h1>-->

<h1 align=center>Available plots for {{app}} app ({{cid}})</h1>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr>
   <th>Title</th> 
   <th>Type</th> 
   <th>Filename</th> 
   <th>X-Column</th> 
   <th>Y-Column</th> 
   <th>Action</th> 
</tr>
</thead>
%for row in rows:
  <tr>
     <td>{{row['plots']['title']}}</td>
     <td>{{row['plots']['ptype']}}</td>
     <td>{{row['plots']['filename']}}</td>
     <td>{{row['plots']['col1']}}</td>
     <td>{{row['plots']['col2']}}</td>
  <td><a href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">plot</a> -
      <a href="/plots/delete/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">delete</a> 
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
       <option VALUE="flot-line">flot/line</option>
       <option VALUE="flot-bar">flot/bar</option>
       <option VALUE="mpl-line">matplotlib/line</option>
       <option VALUE="mpl-bar">matplotlib/bar</option>
   </select><br>
   <input type="hidden" name="app" value="{{app}}">
   <input type="hidden" name="cid" value="{{cid}}">
   <input type="submit">
</form>

%include('footer')
