%include('header')
%include('navbar')

<h1>{{app}} app</h1>

<table class="table table-striped">
  <tr>
      <td>Name:</td> 
      <td><a href="/app/{{rows['name']}}"></a>{{rows['name']}}</td></tr>
  </tr>
  <!-- <tr>
      <td>Category:</td>
      <td>{{rows['category']}}</td>
  </tr> -->
  <tr>
      <td>Description:</th>
      <td>{{rows['description']}}</td>
  </tr>
  <tr>
      <td>Input format:</td>
      <td>{{rows['input_format']}}</td> 
  </tr>
  <!-- <tr>
      <td>Language:</td>
      <td>{{rows['language']}}</td> 
  </tr> -->
  <tr>
      <td>Command:</td> 
      <td>{{rows['command']}}</td> 
  </tr>
</table>

<div class="container-fluid">

<div class="btn-group">
    <!-- <span class="glyphicon glyphicon-trash"></span> -->
    <form class="btn-group" method="post" action="/app/edit/{{rows['id']}}">
        <input type="submit" class="btn btn-default" value="Edit {{app}}">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="hidden" name="edit" value="True">
    </form>
    <form class="btn-group" method="post" action="/appconfig/inputs/upload">
        <input type="submit" class="btn btn-default" value="Configure Inputs">
        <input type="hidden" name="appname" value="{{rows['name']}}">
        <input type="hidden" name="input_format" value="{{rows['input_format']}}">
    </form>
    <form class="btn-group" method="post" action="/appconfig/exe/upload">
        <input type="hidden" name="appname" value="{{rows['name']}}">
        <input type="submit" class="btn btn-default" value="Configure Executable">
    </form>
    <form class="btn-group" method="get" action="/plots/edit">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="submit" class="btn btn-default" value="Configure Plots">
    </form>
    <button type="button" class="btn btn-danger" data-toggle="modal" 
            data-target="#dModal">
            <span class="glyphicon glyphicon-trash"></span> Delete {{app}}</button>
</div>

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
                    <h4 class="modal-title" id="deleteModal">Delete App {{rows['name']}}?</h4>
                    <div class="modal-body">
                      <div class="form-group">
                        <label for="del_app_dir">
                          Delete disk files stored in apps folder?
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
                    <button type="submit" class="btn btn-primary">Delete</button>
                </div>
            </form>
        </div>
    </div>
</div>

</div>

%include('footer')
