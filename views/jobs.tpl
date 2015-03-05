%include('header')
<link type="text/css" rel="StyleSheet" href="/static/css/clickable_rows.css"/>

<body onload="init()">
%include('navbar')
<!--<meta http-equiv="refresh" content="5">-->
%include('tablesorter')
<h1 align=center>{{user}}'s jobs</h1>

<!--<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">-->

<table id="clickable">
<thead>
<tr>
  <th>jid</th> 
  <th>app</th> 
  <th>cid</th> 
  <th>state</th> 
  <th>np</th> 
  <th>description</th>
  <th>date/time submitted</th> 
  <th>shared</th>
</tr>
</thead>

<tbody>
%for row in rows:
  <form>
  <tr>
  <td>{{row['id']}}</td>
  <td>{{row['app']}}</td>
  <td>{{row['cid']}}</td>
  <td>{{row['state']}}</td>
  <td>{{row['np']}}</td>
  <td>{{row['description']}}</td>
  <td>{{row['time_submit']}}
  <a href="/case?cid={{row['cid']}}&app={{row['app']}}&jid={{row['id']}}"></a>
  </td>
  %if row['shared']=="True":
      <td>shared</td>
  %end
</tr> 
%end
</tbody>
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
