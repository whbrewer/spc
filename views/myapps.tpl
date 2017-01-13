%include('header')
<style>
  .panel:hover {
    background-color: #dfdfdf !important;
  }
  a {
    text-decoration: none;
    color: #5f5f5f;
  }
</style>

<body>
%include('navbar')

<div class="row">

  <div class="col-xs-12 col-md-4" align="left">
    <div class="btn-group">
      <a class="btn btn-default active" href="/myapps">Activated</a>
      <a class="btn btn-default" href="/apps">Installed</a>
    </div>
  </div>

</div>

<div style="height:15px"></div>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<div class="container-fluid">

  % if not rows:
    <div class="bs-callout bs-callout-warning">
      <h4>No active apps</h4>
      <p>To activate an app, click "Installed" and activate an app.</p>
    </div>
  % end

  <div id="mypanel" class="panel-group">
    <div class="row">
      % for row in rows:
        <div class="panel panel-primary">
            <button type="button" class="btn btn-link pull-right" onclick="removeapp('{{row['apps.name']}}')" style="color:white"><span class="glyphicon glyphicon-remove"</span></button>

          <div class="panel-heading"><h2>{{row['apps.name']}}</h2>
            <a style="text-decoration:none" href="/{{row['apps.name']}}">
          </div>

          <div class="panel-body"><h4>{{row['apps.description']}}</h4></div>

          <div class="panel-footer">category: {{row['apps.category']}}</a>
            <!-- <a href="javascript:removeapp('{{row['apps.name']}}')"><span class="glyphicon glyphicon-minus-sign"></span></a> -->
            %if configurable:
              <a href="/app/{{row['apps.name']}}"><span style="font-size:150%" class="glyphicon glyphicon-cog"></span></a>
            %end
          </div>

        </div>
      %end
    </div>
  </div>

</div>

<script>
function removeapp(app) {
    $.post('/removeapp', {'app': app});
    location.reload();
}
</script>

%include('footer')
