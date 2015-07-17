%include('header')
<link type="text/css" rel="StyleSheet" href="/static/css/clickable_rows.css"/>

%include('navbar')
%include('navactions')

<h1>{{app}} app</h1>

<table id="clickable" border=0>
  <tr>
      <td>Name:</td> 
      <td><a href="/app/{{rows['name']}}"></a>{{rows['name']}}</td></tr>
  </tr>
  <tr>
      <td>Category:</td>
      <td>{{rows['category']}}</td>
  </tr>
  <tr>
      <td>Description:</th>
      <td>{{rows['description']}}</td>
  </tr>
  <tr>
      <td>Input format:</td>
      <td>{{rows['input_format']}}</td> 
  </tr>
  <tr>
      <td>Language:</td>
      <td>{{rows['language']}}</td> 
  </tr>
  <tr>
      <td>Command:</td> 
      <td>{{rows['command']}}</td> 
  </tr>
</table>

<!--
<table>
<tr> <td>
    <form method="post" action="/app/edit/{{rows['id']}}">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="hidden" name="edit" value="True">
        <input type="submit" value="edit {{app}}">
    </form>
</td><td>
    <form method="post" action="/app/delete/{{rows['id']}}">
        <input type="hidden" name="appname" value="{{rows['name']}}">
        <input type="submit" value="delete {{app}}" 
        onclick="if(confirm('are you sure?')) return true; return false">
    </form>
</td></tr>
-->
</table>

%include('footer')
