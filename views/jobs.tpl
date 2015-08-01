%include('header')

<body onload="init()">
%include('navbar')
<!--<meta http-equiv="refresh" content="5">-->
<h1 align=center>Jobs</h1>

<table id="clickable" class="table table-striped">
<thead>
<tr>
  <th>jid</th> 
  <th>app</th> 
  <th>cid</th> 
  <th>state</th> 
  <th>np</th> 
  <th>priority</th> 
  <th>date/time submitted</th> 
  <th>description</th>
  <th>fav</th>
</tr>
</thead>

<tbody>
%for row in rows:
  <tr>
  <form>
  <td>{{row['id']}}</td>
  <td>{{row['app']}}</td>
  <td>{{row['cid']}}</td>
  <td align="center">{{row['state']}}</td>
  <td align="center">{{row['np']}}</td>
  <td align="center">{{row['priority']}}</td>
  <td>{{row['time_submit']}}</td>
  <td>{{row['description']}}
  <a href="/case?cid={{row['cid']}}&app={{row['app']}}&jid={{row['id']}}"></a>
  </td>
  %if row['shared']=="True":
      <td><span class="glyphicon glyphicon-star"></span></td>
  %else:
      <td></td>
  %end
  </form>
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
