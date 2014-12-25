%include('header')

<body onload="init()">
%include('navbar')

<h1 align=center>Wall</h1>

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
<thead>
<tr> 
   <th>id</th> 
   <th>user</th> 
   <th>app</th> 
   <th>cid</th> 
   <th>comment</th> 
   <th>set</th>
</tr>
</thead>

%for row in rows:
  <tr>
  <td>{{row[0]}}</td>
  <td>{{row[1]}}</td>
  <td>{{row[2]}}</td>
  <td>{{row[3]}}</td>
  <td>{{row[4]}}</td>
  <td><a style="cursor: pointer" onclick="set_cid('{{row[1]}}/{{row[3]}}','{{row[2]}}')"><u>set</u></a></td>
  </tr> 
%end
</table>

%include('footer')
