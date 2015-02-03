%include('header')
%include('navbar')

<table>
<tr><td>
    <form method="get" action="/plots/edit">
        <input type="hidden" name="app" value="{{app}}">
        <input type="hidden" name="cid" value="{{cid}}">
        <input type="submit" value="Edit Plots">
    </form>
</td>
%if defined('cid'):
%if not cid=='':
<td>
    <form method="get" action="/plot/{{pltid}}">
        <input type="hidden" name="app" value="{{app}}">
        <input type="hidden" name="cid" value="{{cid}}">
        <input type="submit" value="Plot">
    </form>
</td>
%end
%end
</tr>
</table>

<h1>Edit Datasources for Plot {{pltid}}</h1>

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
    <thead><tr><th>Label</th><th>Type</th><th>Color</th><th>Filename</th>
               <th>Columns</th><th>Linerange</th><th>actions</th></tr></thead>
    %for row in rows:
    <tr>
        <td contenteditable='true'>{{row['label']}}</td>
        <td>{{row['ptype']}}</td>
        <td>{{row['color']}}</td>
        <td>{{row['filename']}}</td>
        <td>{{row['cols']}}</td>
        <td>{{row['line_range']}}</td>
        <td><form method="post" action="/plots/datasource_delete">
            <input type="hidden" name="dsid" value="{{row['id']}}">
            <input type="hidden" name="pltid" value="{{pltid}}">
            <input type="hidden" name="app" value="{{app}}">
            <input type="hidden" name="cid" value="{{cid}}">
            <input type="submit" value="delete" onclick="if(confirm('confirm')) return true; return false"></form>
    </tr>
    %end 
</table>

<h1>Add a data source to plot {{pltid}}</h1>

<form method="post" action="/plots/datasource_add">
<table padding=10>
   <tr><td>Label:</td> <td><input type="text" name="label"></td></tr>
   <tr><td>Plot type:</td>
   <td><select name="ptype">
       <option VALUE="line">line</option>
       <option VALUE="points">points</option>
       <option VALUE="bars">bars</option>
   </select></td></tr>
   <tr><td>Color:</td>
   <td><select name="color">
       <option VALUE="rgb(200,0,0)">red</option>
       <option VALUE="rgb(0,200,0)">green</option>
       <option VALUE="rgb(0,0,200)">blue</option>
       <option VALUE="rgb(0,0,0)">black</option>
   </select></td></tr>
   <tr><td>Filename:</td> <td><input type="text" name="fn"></td></tr>
   <tr><td>Column range:</td><td><input type="text" name="cols"></td><td><em>e.g. 1:2 to plot columns 1 and 2</em></td></tr>
   <tr><td>Line range:</td><td><input type="text" name="line_range"></td><td><em>e.g. 3:53 to plot only lines 3 to 53</em></tr>
   <tr><td></td><td><input type="submit"></td></tr>
   <input type="hidden" name="pltid" value="{{pltid}}"> 
   <input type="hidden" name="app" value="{{app}}">
   <input type="hidden" name="cid" value="{{cid}}">
</table>
</form>

%include('footer')
