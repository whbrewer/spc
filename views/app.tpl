%include('header')
%include('navbar')

<h1>{{app}} app</h1>

<table class="table table-striped">
  <tr>
      <td>Name:</td> 
      <td><a href="/app/{{rows['name']}}"></a>{{rows['name']}}</td></tr>
  </tr>
  <tr>
      <td>Category:</td>
      <td>{{rows['category']}}</td>
  </tr>
  <tr>
      <td>Description:</th>
      <td>{{rows['description']}}</td>
  </tr>
  <tr>
      <td>Input format:</td>
      <td>{{rows['input_format']}}</td> 
  </tr>
  <tr>
      <td>Language:</td>
      <td>{{rows['language']}}</td> 
  </tr>
  <tr>
      <td>Command:</td> 
      <td>{{rows['command']}}</td> 
  </tr>
</table>

<div class="btn-group">
    <form class="btn-group" method="post" action="/app/edit/{{rows['id']}}">
        <input type="submit" class="btn btn-default" value="Edit {{app}}">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="hidden" name="edit" value="True">
    </form>
    <form class="btn-group" method="get" action="/plots/edit">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="submit" class="btn btn-default" value="Plot configuration">
    </form>
    <button type="button" class="btn btn-default" data-toggle="modal" 
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

%include('footer')
