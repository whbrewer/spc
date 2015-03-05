%include('header')
<link type="text/css" rel="StyleSheet" href="/static/css/clickable_rows.css"/>

<body onload="init()">
%include('navbar')
%include('tablesorter')

<h1 align=center>Shared cases</h1>

<!--<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">-->
<table id="clickable">
<thead>
<tr> 
   <th>job id</th> 
   <th>user</th> 
   <th>app</th> 
   <th>cid</th> 
   <th>comment</th> 
</tr>
</thead>

%for row in rows:
  <tr>
     <td>{{row['id']}}</td>
     <td>{{row['user']}}</td>
     <td>{{row['app']}}</td>
     <td>{{row['cid']}}</td>
     <td>{{row['description']}}
         <a href="/case?cid={{row['user']}}/{{row['cid']}}&app={{row['app']}}&jid={{row['id']}}"></a>
     </td>
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
