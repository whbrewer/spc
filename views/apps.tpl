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

  <div class="col-xs-4" align="left">  
    <div class="btn-group">
        <a class="btn btn-default" href="/myapps">My apps</a>
        <a class="btn btn-default active" href="/apps">Installed apps</a>
    </div>
  </div>

  <div class="col-xs-4">
    <form role="form" action="/apps">
      <input name="q" type="text" class="form-control input-mg"
           onchange="show(this.value)" placeholder="Search for apps...">
    </form>
  </div>

  %if configurable:
  <div class="col-xs-4" align="right">
   <a href="/addapp" class="btn btn-primary">
     <span class="glyphicon glyphicon-plus"></span> Add
   </a>
  </div>
  <div class="col-xs-12" style="height:5px"></div>
  %end
</div>

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
          <button type="button" class="btn btn-success" onclick="useapp('{{row['name']}}')">Activate</button>
          <!-- <a href="javascript:useapp('{{row['name']}}')"><span class="glyphicon glyphicon-plus-sign" onclick="useapp('{{row['name']}}')"></span></a> -->
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
}
</script>

%include('footer')
