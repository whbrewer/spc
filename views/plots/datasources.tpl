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

<style>
  table { font-size: 120%; }
</style>

<div id="warning" align="center" class="alert-warning"></div>

<ol class="breadcrumb">
  <li><a href="/">Home</a></li>
  <li><a href="/app/{{app}}">Configure App</a></li>
  <li><a href="/plots/edit?app={{app}}">Plots</a></li>
  <li class="active">Datasources</li>
</ol>

<div class="row">

  <div class="col-xs-12 col-sm-10"><h1 style="vertical-align:top">Data Sources for Plot {{pltid}}</h1></div>

  <div class="col-xs-12 col-sm-2"><button type="button" class="btn btn-default pull-right" data-toggle="collapse" data-target="#editsource"><span class="glyphicon glyphicon-plus"></span> Add Datasource</button></div>

</div>

<div id="editsource" class="collapse">

<form id="datasourceForm" class="form-horizontal" method="post" action="/plots/{{pltid}}/datasources" onsubmit="return validateForm()">

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
    <button class="btn btn-success center-block">Submit</button>
    <input type="hidden" name="pltid" value="{{pltid}}">
    <input type="hidden" name="app" value="{{app}}">
</form>
</div>

<table class="table table-striped">
    <thead><tr><th>Filename</th><th>Columns</th><th>Line range</th><th>Data definition (JSON)</th><th>actions</th></tr></thead>
    %for row in rows:
    <tr>
        <td>{{row['filename']}}</td>
        <td>{{row['cols']}}</td>
        <td>{{row['line_range']}}</td>
        <td>{{row['data_def']}}</td>
        <td><form method="post" action="/plots/datasource_delete">
              <input type="hidden" name="dsid" value="{{row['id']}}">
              <input type="hidden" name="pltid" value="{{pltid}}">
              <input type="hidden" name="app" value="{{app}}">
              <button type="submit" class="btn btn-link" value="delete" onclick="if(confirm('confirm')) return true; return false"><span style="color:#d9302c" class="glyphicon glyphicon-remove"></span> delete</button>
            </form>
            <form method="get" action="/plots/{{pltid}}/datasources/{{row['id']}}">
              <input type="hidden" name="app" value="{{app}}">
              <button type="submit" class="btn btn-link"><span style="color:#000" class="glyphicon glyphicon-pencil"></span> edit</button>
            </form>
        </td>
    </tr>
    %end
</table>

%include('footer')
