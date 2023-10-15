%rebase('base.tpl')

<ol class="breadcrumb">
  <li><a href="/">Apps</a></li>
  <li><a href="/app/{{app}}">Configure App</a></li>
  <li><a href="/plots/edit?app={{app}}">Plots</a></li>
  <li><a href="/plots/{{pltid}}/datasources?app={{app}}">Datasources</a></li>
  <li class="active">Edit datasource</li>
</ol>

<h1 class="text-center">Edit data source</h1>

<br>

<form id="datasourceForm" class="form-horizontal" method="post" action="/plots/{{pltid}}/datasources/{{dsid}}" onsubmit="return validateForm()">

    <div class="form-group">
        <label for="label" class="control-label col-md-3">Label:</label>
        <div class="col-md-6">
            <input type="text" class="form-control input-lg" name="label" id="label" value="{{row['label']}}">
        </div>
    </div>

    <div class="form-group">
        <label for="data_def" class="control-label col-md-3">Data definition (JSON):</label>
        <div class="col-md-6"><textarea style="font-size:120%" class="form-control" name="data_def" id="data_def">{{row['data_def']}}</textarea></div>
    </div>

    <div class="form-group">
        <label for="filename" class="control-label col-md-3">Filename:</label>
        <div class="col-md-6"><input type="text" class="form-control input-lg" name="fn" id="filename" value="{{row['filename']}}" required></div>
    </div>

    <div class="form-group">
        <label for="cols" class="control-label col-md-3">Columns (e.g. 1:2):</label>
        <div class="col-md-6"><input type="text" class="form-control input-lg" id="cols" name="cols" value="{{row['cols']}}" pattern="\d+:\d+" required></div>
    </div>

    <div class="form-group">
        <label for="line_range" class="control-label col-md-3">Line range (e.g. 3-53):</label>
        <div class="col-md-6"><input type="text" class="form-control input-lg" id="line_range" name="line_range" value="{{row['line_range']}}" pattern="-?\d+:\d+"></div>
    </div>
    <button class="btn btn-success center-block">Submit</button>
    <input type="hidden" name="pltid" value="{{pltid}}">
    <input type="hidden" name="app" value="{{app}}">

</form>
