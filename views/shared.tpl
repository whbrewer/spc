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
     <td>{{row['shared']['jid']}}</td>
     <td>{{row['jobs']['user']}}</td>
     <td>{{row['jobs']['app']}}</td>
     <td>{{row['jobs']['cid']}}</td>
     <td>{{row['shared']['comment']}}
         <a href="/case?cid={{row['jobs']['user']}}/{{row['jobs']['cid']}}&app={{row['jobs']['app']}}&sid={{row['shared']['id']}}&jid={{row['shared']['jid']}}"></a>
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
