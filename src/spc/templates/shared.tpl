<%
    style = """
        .glyphicon.glyphicon-star, .glyphicon.glyphicon-star-empty {
            font-size: 120%;
        }
        .table {
            font-size: 120%;
        }
    """
    rebase('base.tpl', style=style)
%>

<h1 class="text-center">Shared Cases</h1>

<table id="clickable" class="table table-striped">
<thead>
<tr>
   <th>cid</th>
   <th>user</th>
   <th>app</th>
   <th class="hidden-xs">time/date</th>
   <th class="hidden-xs">labels</th>
</tr>
</thead>

%for row in rows:
  <tr>
     <td><samp>{{row['jobs.cid']}}</samp></td>
     <td><samp>{{row['users.user']}}</samp></td>
     <td><samp>{{row['jobs.app']}}</samp></td>
     <td class="case hidden-xs"><samp>{{row['jobs.time_submit']}}</samp> </td>
     <td class="hidden-xs"><samp>{{row['jobs.description']}}</samp>
         <a href="/case?cid={{row['users.user']}}/{{row['jobs.cid']}}&app={{row['jobs.app']}}&jid={{row['jobs.id']}}"></a>
     </td>
  </tr>
%end
</table>

<form method="get" action="/jobs/shared">
  <input type="hidden" name="n" value="{{n+num_rows}}">
  <input type="submit" class="btn btn-default btn-block" value="Show more">
</form>

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
