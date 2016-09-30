%include('header')
%include('navbar')

<script>
function ddef() {
  l = document.getElementById("label").value
  ls = "label: \"" + l + "\""
  ds = "data: d" + {{len(rows)+1}}
  ptype = document.getElementById("ptype").value
  if (ptype == "line") {
    ps = "lines: { show: true }"
  } else if (ptype == "bars") {
    ps = "bars: { show: true, autoWidth: true }"
  } else {
    ps = "points: { show: true }"
  }
  c = document.getElementById("color").value
  cs = "color: \"" + c + "\"" 
  document.getElementById("data_def").value = 
    "{" + ls + ", " + ds + ", "+ ps + ", " + cs + "}"
}
</script>

<div id="warning" align="center" class="alert-warning"></div>

<div align="left" class="container-fluid">
    <div class="row">
        <div class="btn-group align-center">
            <form class="btn-group" method="get" action="/plots/edit">
                    <button class="btn btn-default"><span class="glyphicon glyphicon-chevron-left"></span> Edit Plots</button>
                    <input type="hidden" name="app" value="{{app}}">
                    <input type="hidden" name="cid" value="{{cid}}">
                </form>
            <button type="button" class="btn btn-default" data-toggle="collapse" data-target="#editsource">Add Data Source</button>
            %if defined('cid'):
            %if not cid=='':
            <form class="btn-group" method="get" action="/plot/{{pltid}}">
                <input type="hidden" name="app" value="{{app}}">
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="submit" class="btn btn-default" value="Plot">
            </form>
            %end
            %end
        </div>
    </div>
</div>

<div id="editsource" class="collapse">

<form id="datasourceForm" class="form-horizontal" method="post" action="/plots/datasource_add" onsubmit="return validateForm()">

    <div class="form-group">
        <label for="label" class="control-label col-md-3">Label:</label>
        <div class="col-md-6">
            <input type="text" class="form-control" name="label" id="label" onchange="ddef()" required>
        </div>
    </div>

    <div class="form-group">
        <label for="ptype" class="control-label col-md-3">Plot type:</label>
        <div class="col-md-6">
           <select name="ptype" id="ptype" class="form-control" onchange="ddef()">
               <option VALUE="line">line</option>
               <option VALUE="points">points</option>
               <option VALUE="bars">bars</option>
           </select>
        </div>
    </div>

    <div class="form-group">
        <label for="color" class="control-label col-md-3">Color:</label>
        <div class="col-md-6">
            <select name="color" id="color" class="form-control" onchange="ddef()">
                <option VALUE="rgb(200,0,0)">red</option>
                <option VALUE="rgb(0,200,0)">green</option>
                <option VALUE="rgb(0,0,200)">blue</option>
                <option VALUE="rgb(0,0,0)">black</option>
            </select>
        </div>
    </div>

    <div class="form-group">
        <label for="data_def" class="control-label col-md-3">Data definition (JSON):</label>
        <div class="col-md-6"><textarea class="form-control" name="data_def" id="data_def"></textarea></div>
    </div>

    <div class="form-group">
        <label for="filename" class="control-label col-md-3">Filename:</label>
        <div class="col-md-6"><input type="text" class="form-control" name="fn" required></div>
    </div>

    <div class="form-group">
        <label for="cols" class="control-label col-md-3">Column range (e.g. 1:2):</label>
        <div class="col-md-6"><input type="text" class="form-control" id="cols" name="cols" pattern="\d+:\d+" required></div>
    </div>

    <div class="form-group">
        <label for="line_range" class="control-label col-md-3">Line range (e.g. 3:53):</label>
        <div class="col-md-6"><input type="text" class="form-control" id="line_range" name="line_range" pattern="\d+:\d+" required></div>
    </div>
    <button class="btn btn-primary">Submit</button>
    <input type="hidden" name="pltid" value="{{pltid}}"> 
    <input type="hidden" name="app" value="{{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
</form>
</div>

<h1 align="center">Data Sources for Plot {{pltid}}</h1>

<table class="table table-striped">
    <thead><tr><th>Filename</th><th>Columns</th><th>Line range</th><th>Data definition (JSON)</th><th>actions</th></tr></thead>
    %for row in rows:
    <tr>
        <td contenteditable='true'>{{row['filename']}}</td>
        <td>{{row['cols']}}</td>
        <td>{{row['line_range']}}</td>
        <td>{{row['data_def']}}</td>
        <td><form method="post" action="/plots/datasource_delete">
            <input type="hidden" name="dsid" value="{{row['id']}}">
            <input type="hidden" name="pltid" value="{{pltid}}">
            <input type="hidden" name="app" value="{{app}}">
            <input type="hidden" name="cid" value="{{cid}}">
            <input type="submit" class="btn btn-default" value="delete" onclick="if(confirm('confirm')) return true; return false"></form>
    </tr>
    %end 
</table>

%include('footer')
