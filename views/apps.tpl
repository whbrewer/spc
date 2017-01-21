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
      <a class="btn btn-warning" href="/myapps">Activated</a>
      <a class="btn btn-warning active" href="/apps">Installed</a>
    </div>
  </div>

  <div class="hidden-xs col-md-4">
    <form role="form" action="/apps">
      <input name="q" type="text" class="form-control input-lg"
             onchange="show(this.value)" placeholder="Search for apps...">
    </form>
  </div>

  %if configurable:
  <div class="xs-hidden col-md-4" align="right">
    <a href="/addapp" class="btn btn-primary">
      <span class="glyphicon glyphicon-plus"></span> Add
    </a>
  </div>
  %end
</div>

<div style="height:5px"></div>

%# template to generate a HTML table from a list of tuples
%# from bottle documentation 0.12-dev p.53

<div class="container-fluid">

  <div id="mypanel" class="panel-group">
    <div class="row">
      % for row in rows:
        <div class="panel panel-info">
          <div class="panel-heading"><h2>{{row['name']}}</h2></div>
          <div class="panel-body"><h4>{{row['description']}}</h4></div>
          <div class="panel-footer">category: {{row['category']}}</div>

          % if row['id'] in activated:
            <button type="button" class="btn btn-info" disabled="true">Activated</button>
          % else:
            <button type="button" class="btn btn-success" onclick="useapp('{{row['name']}}')">Activate</button>
          % end

          %if configurable:
            <a href="/app/{{row['name']}}"><span style="font-size:150%" class="glyphicon glyphicon-cog"></span></a>
          %end
        </div>
      <br>
      %end
    </div>
  </div>
</div>

<script>
function useapp(app) {
  $.post('/useapp', {'app': app})
  location.reload();
}
</script>

%include('footer')
