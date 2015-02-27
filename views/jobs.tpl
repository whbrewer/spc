%include('header')
<link type="text/css" rel="StyleSheet" href="/static/css/clickable_rows.css"/>

<body onload="init()">
%include('navbar')
<!--<meta http-equiv="refresh" content="5">-->
%include('tablesorter')
<h1 align=center>{{user}}'s jobs</h1>

<!--<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">-->

<script>
 function showMenu(){
   document.getElementById("actions").style.display="block";
 }
 function hideMenu(){
   document.getElementById("actions").style.display="none";
 }
</script>

<div id="actions" style="display:none">
<a href="">monitor</a> ::
<a href="">stop</a> ::
<a href="">files</a> ::
<a href="">zipcase</a> ::
<a href="">start</a> ::
<a href="">delete</a> ::
<a href="">post</a> ::
</div>

<table id="clickable">
<thead>
<tr>
  <th>jid</th> 
  <th>app</th> 
  <th>cid</th> 
  <th>state</th> 
  <th>np</th> 
  <th>time_submit</th> 
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
  <td>{{row['time_submit']}}
      <a href="/case?cid={{row['cid']}}&app={{row['app']}}&jid={{row['id']}}">
      </a>
  </td>
      <!--<a href="" onclick="showMenu()"></a>-->
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
