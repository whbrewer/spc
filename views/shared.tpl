%include('header')

<style>
  .glyphicon.glyphicon-star, .glyphicon.glyphicon-star-empty {
    font-size: 120%;
  }
  .table {
    font-size: 120%;
  }
</style>
</head>

<body onload="init()">
%include('navbar')

<h1 align=center>Shared Cases</h1>

<table id="clickable" class="table table-striped">
<thead>
<tr> 
   <th>cid</th> 
   <th>user</th> 
   <th>app</th> 
   <th class="hidden-xs">labels</th> 
</tr>
</thead>

%for row in rows:
  <tr>
     <td>{{row['jobs.cid']}}</td>
     <td>{{row['users.user']}}</td>
     <td>{{row['jobs.app']}}</td>
     <td class="hidden-xs">{{row['jobs.description']}}
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

%include('footer')
