%include('header')
%include('navbar')

<body>

<script>
function opt() {
  xl = document.getElementById("xaxis_label").value;
  xstr = "xaxis: { axisLabel: \"" + xl + "\"}"
  yl = document.getElementById("yaxis_label").value;
  ystr = "yaxis: { axisLabel: \"" + yl + "\"}"
  // don't set options for categories plot b/c it will not work correctly
  var e = document.getElementById("ptype")
  var strUser = e.options[e.selectedIndex].value;
  if (strUser != "flot-cat") {
    document.getElementById("options").value =
      "legend: { position: \"nw\"}" + ", " + xstr + ", " + ystr;
  }
}

function leg(val) {
  legpos = document.getElementById("legpos")
  legstr = "legend: { position: \"" + val + "\"}"
  opt()
}

function endis() {
  // disable options for categories plot b/c it will not work correctly
  var e = document.getElementById("ptype")
  var strUser = e.options[e.selectedIndex].value;
  if (strUser == "flot-cat") {
    document.getElementById("options").readOnly = true;
  } else {
    document.getElementById("options").readOnly = false;
  }
}
</script>

<style type="text/css">
  td,th {
    text-align: center
  }
  table {
    font-size: 120%;
  }
</style>

<ol class="breadcrumb">
  <li><a href="/">Apps</a></li>
  <li><a href="/app/{{app}}">Configure App</a></li>
  <li class="active">Plots</li>
</ol>

<div class="row">

  <div class="col-xs-12 col-sm-10"><h1 style="vertical-align:top">Plot definitions for {{app}} app</h1></div>

  <div class="col-xs-12 col-sm-2"><button type="button" class="btn btn-default pull-right" data-toggle="collapse" data-target="#addplot"><span class="glyphicon glyphicon-plus"></span> Add Plot</button></div>

</div>

<div class="container-fluid">

<div id="addplot" class="collapse">
<form class="form-horizontal" method="post" action="/plots/create">
    <div class="form-group">
        <label for="title" class="control-label col-md-3">Title:</label>
        <div class="col-md-6"><input type="text" class="form-control" name="title"></div>
    </div>

    <div class="form-group">
        <label for="ptype" class="control-label col-md-3">Type of plot:</label>
        <div class="col-md-6">
            <select name="ptype" id="ptype" class="form-control" onchange="endis()">
                <option VALUE="flot-scatter">flot/scatter (line, bar, points)</option>
                <option VALUE="flot-scatter-animated">flot/scatter animated</option>
                <option VALUE="flot-cat">flot/categories</option>
                <option VALUE="plotly-hist">plotly/histogram</option>
                <option VALUE="mpl-line">matplotlib/line</option>
                <option VALUE="mpl-bar">matplotlib/bar</option>
            </select>
        </div>
    </div>

    <!--
    <fieldset>
      <legend>legend position:</label>
      <input type="radio" name="legpos" value="ne" onclick="leg(this.value)"> ne
      <input type="radio" name="legpos" value="nw" onclick="leg(this.value)"> nw
      <input type="radio" name="legpos" value="se" onclick="leg(this.value)"> se
      <input type="radio" name="legpos" value="sw" onclick="leg(this.value)"> sw
    </fieldset>
    -->

    <div class="form-group">
      <label class="control-label col-md-3">xaxis label:</label>
      <div class="col-md-6">
        <input type="text" class="form-control" name="xaxis_label" id="xaxis_label" onchange="opt()">
      </div>
    </div>

    <div class="form-group">
      <label class="control-label col-md-3">yaxis label:</label>
      <div class="col-md-6">
        <input type="text" class="form-control" name="yaxis_label" id="yaxis_label" onchange="opt()">
      </div>
    </div>

    <div class="form-group">
        <label for="options" class="control-label col-md-3">Options (JSON):</label>
        <div class="col-md-6">
            <textarea name="options" id="options" class="form-control"></textarea>
        </div>
    </div>

    <input type="submit" class="btn btn-success center-block" value="Submit">
    <input type="hidden" name="app" value="{{app}}">
</form>
</div>
</div>

<table id="clickable" class="table table-striped">
<thead>
<tr>
   <th>#</th>
   <th>Title</th>
   <th>Type</th>
   <th>Options</th>
   <th> </th>
</tr>
</thead>
% i = 0
% for row in rows:
% i += 1
<tr>
    <!-- <td>{{row['plots']['id']}}</td> -->
    %url="/plots/"+str(row['plots']['id'])+"/datasources?app="+app
    <td class="plotdef">{{i}} <a href="{{url}}"></a></td>
    <td class="plotdef">{{row['plots']['title']}} <a href="{{url}}"></a></td>
    <td class="plotdef" width="50">{{row['plots']['ptype']}} <a href="{{url}}"></a></td>
    <td class="plotdef">{{row['plots']['options']}} <a href="{{url}}"></a>
    <td style="vertical-align:middle">
        <div class="dropdown">
            <button class="btn btn-link dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
                <i class="glyphicon glyphicon-option-vertical"></i>
            </button>
            <ul class="dropdown-menu pull-right">
                <li><a  href="/plots/{{row['plots']['id']}}/datasources?app={{app}}">Datasources</a></li>
                <li><a href="/plots/delete/{{row['plots']['id']}}?app={{app}}" onclick="if(confirm('confirm')) return true; return false"> Delete</a></li>
                <li><a href="/plots/edit/{{row['plots']['id']}}?app={{app}}"> Edit</a></li>
            </ul>
        </div>
    </td>
</tr>
% end
</table>

<script>
$(document).ready(function() {
    $('.plotdef').click(function(e) {
        var href = $(this).find("a").attr("href");
        if(href) { window.location = href; }
        e.stopPropagation();
    });
});
</script>

%include('footer')
