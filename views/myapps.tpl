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

<div style="height:15px"></div>

<div class="row">

  <div class="col-xs-12 col-md-4" align="left">
    <div class="btn-group">
      <a class="btn btn-warning active" href="/myapps">Activated</a>
      <a data-step="2" data-intro="By clicking here you can find apps to run" class="btn btn-warning" href="/apps">Installed</a>
    </div>
  </div>

  <div class="hidden-xs col-md-8">
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

  <div id="mypanel" class="panel-group">
    <div class="row">
      % for row in rows:
        <div class="panel panel-primary">
            <button type="button" class="btn btn-link pull-right" onclick="removeapp('{{row['apps.name']}}')" style="color:white"><span class="glyphicon glyphicon-remove"</span></button>

          <div class="panel-heading"><h2><a href="/{{row['apps.name']}}" style="text-decoration:none; color:white">{{row['apps.name']}}</a></h2>
            <a style="text-decoration:none" href="/{{row['apps.name']}}">
          </div>

          <div class="panel-body"><h4>{{row['apps.description']}}</h4></div>

          <div class="panel-footer">category: {{row['apps.category']}}</a>
            <!-- <a href="javascript:removeapp('{{row['apps.name']}}')"><span class="glyphicon glyphicon-minus-sign"></span></a> -->
            %if configurable:
              <a href="/app/{{row['apps.name']}}"><span style="font-size:150%" class="glyphicon glyphicon-cog pull-right"></span></a>
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

// $(function() {
//   introJs().start();
// })

</script>

%include('footer')
