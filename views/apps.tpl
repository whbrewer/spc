%include('header')
<link type="text/css" rel="StyleSheet" href="/static/css/clickable_rows.css"/>

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
%include('tablesorter')

<h1>Installed Apps</h1>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<form method="get" action="/addapp">
   <input type="submit" class="submit add" value="add">
   <input type="submit" formaction="/apps/load" class="submit start" value="load">
</form>

<!--<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">-->
<table id="clickable">
<thead>
<tr> 
<th>Name</th> 
<th>Tags</th>
<th>Description</th> 
<!-- <th>Input format</th> -->
<!-- <th>Language</th> -->
<!-- <th>Command Line</th> -->
<!-- <th>Actions</th> -->
</tr>
</thead>

%for row in rows:
  <tr>
  <td><a href="/app/{{row['name']}}"></a>{{row['name']}}</td>
  <td>{{row['category']}}</td>
  <td>{{row['description']}}</td>
  <!-- <td>{{row['input_format']}}</td> -->
  <!-- <td>{{row['language']}}</td> -->
  <!-- <td>{{row['command']}}</td> -->
  <!--
  <form method="post" action="/apps/delete/{{row['id']}}">
     <input type="hidden" name="appname" value="{{row['name']}}">
     <td><input type="submit" value="delete" 
          onclick="if(confirm('are you sure you want to delete?')) return true; return false"></td> 
  </form>
  -->
</tr> 
%end
</table>

<script>
$(document).ready(function() {
    $('#clickable tr').click(function() {
        var href = $(this).find("a").attr("href");
        if(href) {
            window.location = href;
        }
    });

});
</script>

%include('footer')
