%include('header')

<body onload="init()">
%include('navbar')
%include('tablesorter')

<h1 align=center>Wall</h1>

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr> 
   <th>job id</th> 
   <th>user</th> 
   <th>app</th> 
   <th>cid</th> 
   <th>comment</th> 
   <th>actions</th>
</tr>
</thead>

%for row in rows:
  <tr>
     <td>{{row['wall']['jid']}}</td>
     <td>{{row['jobs']['user']}}</td>
     <td>{{row['jobs']['app']}}</td>
     <td>{{row['jobs']['cid']}}</td>
     <td>{{row['wall']['comment']}}</td>
     <!--<td><a style="cursor: pointer" onclick="set_cid('{{row['jobs']['user']}}/{{row['jobs']['cid']}}','{{row['jobs']['app']}}')"><u>set</u></a></td>-->
     <td>
        <a href="/start?cid={{row['jobs']['user']}}/{{row['jobs']['cid']}}&app={{row['jobs']['app']}}">start</a> - 
        <a href="/plot/0?cid={{row['jobs']['user']}}/{{row['jobs']['cid']}}&app={{row['jobs']['app']}}">plot</a> - 
        <a href="/files?cid={{row['jobs']['user']}}/{{row['jobs']['cid']}}&app={{row['jobs']['app']}}">files</a> - 
        <a href="/wall/delete/{{row['wall']['id']}}?cid={{row['jobs']['user']}}/{{row['jobs']['cid']}}&app={{row['jobs']['app']}}" onclick="if('{{user}}'=='{{row['jobs']['user']}}') return true; alert('ERROR: wrong user'); return false">delete</a>
     </td>
  </tr> 
%end
</table>

%include('footer')
