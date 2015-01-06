%include('header')

<body onload="init()">
%include('navbar')

<h1 align=center>Wall</h1>

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr> 
   <th>job id</th> 
   <th>user</th> 
   <th>app</th> 
   <th>cid</th> 
   <th>comment</th> 
   <th>set</th>
</tr>
</thead>

%for row in rows:
  <tr>
     <td>{{row['wall']['jid']}}</td>
     <td>{{row['jobs']['user']}}</td>
     <td>{{row['jobs']['app']}}</td>
     <td>{{row['jobs']['cid']}}</td>
     <td>{{row['wall']['comment']}}</td>
     <td><a style="cursor: pointer" onclick="set_cid('{{row['jobs']['user']}}/{{row['jobs']['cid']}}','{{row['jobs']['app']}}')"><u>set</u></a></td>
  </tr> 
%end
</table>

%include('footer')
