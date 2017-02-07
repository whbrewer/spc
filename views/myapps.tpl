%include('header')
<style>
  .panel:hover {
    background-color: #dfdfdf !important;
  }
  a {
    text-decoration: none;
    color: #5f5f5f;
  }
  body {
    background: #f5f5f5 !important;
  }
  .list-group-item {
    font-size: 200%;
  }
</style>

<body>
%include('navbar')

<div style="height:15px"></div>

<div class="row">

  <div class="col-xs-12 col-sm-4" align="left">
    <div class="btn-group">
      <a class="btn btn-warning active" href="/myapps">Activated</a>
      <a data-step="2" data-intro="By clicking here you can find apps to run" class="btn btn-warning" href="/apps">Installed</a>
    </div>
  </div>

  <div class="col-sm-4">
    <h2 align="center">Activated Apps</h2>
  </div>

  <div class="hidden-xs col-sm-4">
     <a class="btn btn-success pull-right" href="javascript:void(0)" onclick="introJs().start()"><span class="glyphicon glyphicon-plane"></span> Take Tour</a>
  </div>
</div>

<div style="height:15px"></div>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<div class="container-fluid">

  % if not rows:
    <div data-step="1" data-intro="Welcome to SPC! You'll first need to activate an app to use." class="bs-callout bs-callout-warning">
      <h4>No active apps</h4>
      <p>To activate an app, click "Installed" and activate an app.</p>
    </div>
  % end

  <div class="list-group">
  % for row in rows:
    % if row['apps.name'] == app:
      <a class="list-group-item active" href="/{{row['apps.name']}}">
    % else:
      <a class="list-group-item" href="/{{row['apps.name']}}">
    % end
      {{row['apps.name']}}
    </a>
  % end
  </div>

</div>

<script>
function removeapp(app) {
    $.post('/removeapp', {'app': app});
    location.reload();
}
</script>

%include('footer')
