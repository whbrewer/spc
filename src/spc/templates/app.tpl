<%
    style = """
        .table {
            font-size: 120%;
        }
        tr:hover {
            cursor: auto;
        }
    """
    rebase('base.tpl', style=style)
%>

<script>
$(document).ready(function() {
   jQuery.ajax({
      type: "get",
      data: { app: '{{app}}' },
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      url:  "/appconfig/status",
      complete: function(xhr){
        var response = JSON.parse(xhr.responseText);
        toggle(response.command,"db")
        toggle(response.inputs,"in")
        toggle(response.template,"tp")
        toggle(response.binary,"bn")
        toggle(response.plots,"pl")
      }
   })
})

function toggle(cmd,id) {
   if (cmd == 1) {
      $("#"+id).addClass('glyphicon-ok')
      $("#"+id).removeClass('glyphicon-remove')
      $("#"+id+"div").toggleClass('has-error', false);
      $("#"+id+"div").toggleClass('has-success', true);
   } else {
      $("#"+id).removeClass('glyphicon-ok')
      $("#"+id).addClass('glyphicon-remove')
      $("#"+id+"div").toggleClass('has-error', true);
      $("#"+id+"div").toggleClass('has-success', false);
   }
}
</script>

<ol class="breadcrumb">
  <li><a href="/">Apps</a></li>
  <li class="active">Configure App</li>
</ol>

<h1>{{app}} app</h1>

<table class="table table-striped">
  <tr>
      <td>Name:</td>
      <td><a href="/app/{{rows['name']}}"></a>{{rows['name']}}</td>
  </tr>
  <tr>
      <td>Category:</td>
      <td>{{rows['category']}}</td>
  </tr>
  <tr>
      <td>Description:</td>
      <td>{{rows['description']}}</td>
  </tr>
  <tr>
      <td>Input format:</td>
      <td>{{rows['input_format']}}</td>
  </tr>
  <tr>
      <td>Pre-process:</td>
      <td>{{rows['preprocess']}}</td>
  </tr>
  <tr>
      <td>Post-process:</td>
      <td>{{rows['postprocess']}}</td>
  </tr>
  <tr>
      <td>Language:</td>
      <td>{{rows['language']}}</td>
  </tr>
  <tr>
      <td>Command:</td>
      <td>{{rows['command']}}</td>
  </tr>
  <tr>
      <td>Static Assets:</td>
      <td>{{rows['assets']}}</td>
  </tr>
</table>

<div class="container-fluid">

<div class="btn-group">
    <!-- <span class="glyphicon glyphicon-trash"></span> -->
    <form class="btn-group" method="post" action="/app/edit/{{rows['id']}}">
        <input type="submit" class="btn btn-default" value="Edit">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="hidden" name="edit" value="True">
    </form>
    <form class="btn-group" method="post" action="/appconfig/inputs/upload">
        <input type="submit" class="btn btn-default" value="Inputs">
        <input type="hidden" name="appname" value="{{rows['name']}}">
        <input type="hidden" name="input_format" value="{{rows['input_format']}}">
    </form>
    <form class="btn-group" method="post" action="/appconfig/exe/upload">
        <input type="hidden" name="appname" value="{{rows['name']}}">
        <input type="submit" class="btn btn-default" value="Executable">
    </form>
    <form class="btn-group" method="get" action="/plots/edit">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="submit" class="btn btn-default" value="Plots">
    </form>
    <form class="btn-group" method="post" action="/appconfig/export">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="submit" class="btn btn-default" value="Export">
    </form>
    <button type="button" class="btn btn-danger" data-toggle="modal"
            data-target="#dModal">
            <span class="glyphicon glyphicon-trash"></span> Delete</button>
</div>

<form>
<h3>Status of installation:</h3>
<div class="form-group" id="dbdiv"><span id="db" class="glyphicon glyphicon-ok"></span> Database entry setup</div>
<div class="form-group" id="indiv"><span id="in" class="glyphicon glyphicon-ok"></span> Inputs file uploaded</div>
<div class="form-group" id="tpdiv"><span id="tp" class="glyphicon glyphicon-ok"></span> HTML template file setup</div>
<div class="form-group" id="bndiv"><span id="bn" class="glyphicon glyphicon-ok"></span> Application binary uploaded</div>
<div class="form-group" id="pldiv"><span id="pl" class="glyphicon glyphicon-ok"></span> Plots setup</div>
</form>

<!-- Delete Modal -->
<div class="modal fade" id="dModal" tabindex="-1" role="dialog"
     aria-labelledby="deleteModal">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <form class="form-horizontal" method="post" action="/app/delete/{{rows['id']}}">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" id="deleteModal">Delete App?</h4>
                    <div class="modal-body">
                      <div class="form-group">
                        <label for="del_app_dir">
                          Delete associated files for app?
                        </label>
                        <input type="checkbox" id="del_app_dir" name="del_app_dir"/>
                      </div>
                      <!-- <div class="form-group">
                        <label for="del_app_cases">
                          Delete {{rows['name']}} cases from disk?
                        </label>
                        <input type="checkbox" id="del_app_cases" name="del_app_cases"/>
                      </div> -->
                    </div>
                    <input type="hidden" name="app" value="{{app}}">
                    <input type="hidden" name="cid" value="{{cid}}">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-danger">Delete</button>
                </div>
            </form>
        </div>
    </div>
</div>

</div>
