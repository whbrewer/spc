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
   <th>job id</th> 
   <th>user</th> 
   <th>app</th> 
   <th>cid</th> 
   <th class="hidden-xs">labels</th> 
</tr>
</thead>

%for row in rows:
  <tr>
     <td>{{row['id']}}</td>
     <td>{{row['user']}}</td>
     <td>{{row['app']}}</td>
     <td>{{row['cid']}}</td>
     <td class="hidden-xs">{{row['description']}}
         <a href="/case?cid={{row['user']}}/{{row['cid']}}&app={{row['app']}}&jid={{row['id']}}"></a>
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
