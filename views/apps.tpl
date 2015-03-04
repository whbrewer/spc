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

<table id="clickable">
<thead>
<tr> 
<th>Name</th> 
<th>Category</th>
<th>Description</th> 
</tr>
</thead>

%for row in rows:
  <tr>
  <td><a href="/app/{{row['name']}}"></a>{{row['name']}}</td>
  <td>{{row['category']}}</td>
  <td>{{row['description']}}</td>
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
