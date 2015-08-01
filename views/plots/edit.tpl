%include('header')
%include('navbar')

<body onload="init()">

<style type="text/css">
td {text-align: center}
</style>

<!--<h1>{{app}}</h1>-->

<h1 align=center>Plot definitions for {{app}} app</h1>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<table class="table table-striped">
<thead>
<tr>
   <th>id</th>
   <th>Title</th> 
   <th>Type</th> 
   <th>Options</th> 
   <th>Data Definition</th> 
   <th>Action</th> 
</tr>
</thead>
%for row in rows:
  <tr>
     <td>{{row['plots']['id']}}</td>
     <td>{{row['plots']['title']}}</td>
     <td width="50">{{row['plots']['ptype']}}</td>
     <td>{{row['plots']['options']}}</td>
     <td>{{row['plots']['datadef']}}</td>
     <td width="100">
        %if not cid == '':
            <a href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">plot</a> <br><br>
        %end
        <a href="/plots/delete/{{row['plots']['id']}}?app={{app}}&cid={{cid}}" 
           onclick="if(confirm('confirm')) return true; return false">delete</a> <br><br>
        <a href="/plots/datasource/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">datasource</a>
     </td>

  <!--
  <form method="get" action="/apps/delete/{row[0]}}">
     <td><input type="button" value="delete"></td> 
  </form>
  -->
</tr> 
%end
</table>

<hr>

<div class="container-fluid">

<button type="button" class="btn btn-default" data-toggle="collapse" 
        data-target="#addplot">Add Plot</button>

<div id="addplot" class="collapse">
<form class="form-horizontal" method="post" action="/plots/create">
    <div class="form-group">
        <label for="title" class="control-label col-md-3">Title:</label>
        <div class="col-md-6"><input type="text" name="title"></div>
    </div>

    <div class="form-group">
        <label for="ptype" class="control-label col-md-3">Type of plot:</label>
        <div class="col-md-6">
            <select name="ptype">
                <option VALUE="flot-line">flot/line</option>
                <option VALUE="flot-cat">flot/categories</option>
                <option VALUE="mpl-line">matplotlib/line</option>
                <option VALUE="mpl-bar">matplotlib/bar</option>
            </select>
        </div>
    </div>

    <div class="form-group">
        <label for="options" class="control-label col-md-3">Options:</label>
        <div class="col-md-6">
            <textarea name="options"></textarea>
        </div>
    </div>

    <div class="form-group">
        <label for="datadef" class="control-label col-md-3">Data definition:</label>
        <div class="col-md-6">
            <textarea name="datadef"></textarea>
        </div>
    </div>

    <input type="submit" class="btn btn-primary" value="Submit">
    <input type="hidden" name="app" value="{{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
</form>
</div>
</div>

%include('footer')
