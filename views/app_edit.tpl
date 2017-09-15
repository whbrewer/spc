%rebase('base.tpl')

<ol class="breadcrumb">
  <li><a href="/">Apps</a></li>
  <li><a href="/app/{{app}}">Configure App</a></li>
  <li class="active">Edit App</li>
</ol>

<h1>{{app}} app</h1>

<form class="form-horizontal" method="post" action="/app/save/{{rows['id']}}">

<table>
  <tr>
      <td>Category:</td>
      <td><input class="form-control input-lg" type="text" name="category"
                 value="{{rows['category']}}"></td>
  </tr>
  <tr>
      <td>Description:</td>
      <td><textarea style="font-size:120%" class="form-control" name="description" cols="60" rows="4">{{rows['description']}}</textarea></td>
  </tr>
  <tr>
      <td>Input format:</td>
      <td><select class="form-control input-lg" name="input_format">
          %opts = {'namelist':'namelist.input','ini':'INI','xml':'XML','json':'JSON', 'yaml':'YAML', 'toml':'TOML'}
          %for key, value in opts.iteritems():
              %if key == rows['input_format']:
                  <option selected value="{{key}}">{{value}}
              %else:
                  <option value="{{key}}">{{value}}
              %end
          %end
      </select>
      </td>
  </tr>
  <tr>
      <td>Pre-process:</td>
      <td><input class="form-control input-lg" type="text" name="preprocess"
                 value="{{rows['preprocess']}}"></td>
  </tr>
  <tr>
      <td>Post-process:</td>
      <td><input class="form-control input-lg" type="text" name="postprocess"
                 value="{{rows['postprocess']}}"></td>
  </tr>
  <tr>
      <td>Language:</td>
      <td><input class="form-control input-lg" type="text" name="language"
                 value="{{rows['language']}}"></td>
  </tr>
  <tr>
      <td>Static Assets:</td>
      <td><input class="form-control input-lg" type="text" name="assets" size="40"
                 value="{{rows['assets']}}"></td>
  </tr>
</table>
<div class="row">
    <div class="col-md-12 col-md-offset-2">
        <input type="hidden" name="app" value="{{rows['name']}}">
        <input type="submit" class="btn btn-success" value="Save changes">
        <a class="btn btn-link" href="/app/{{app}}">Cancel</a>
    </div>
</div>
</form>
