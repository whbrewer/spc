%include('header', title='Menu')

<body>
<style>
  a { font-size: 120% }
</style>

<script>
    function toggle(source) {
      checkboxes = document.getElementsByName('selected_files');
      for(var i=0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
      }
    }

    function toggle_delete_button_visibility() {
      var checkboxes = document.getElementsByName('selected_files');
      var show = false;
      var values = "";
      for(var i=0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
          show = true;
          values += checkboxes[i].value;
        }
      }

      var dom = document.getElementById("actions")
      if (show) {
        dom.style.display = "block";
      } else {
        dom.style.display = "none";
      }

      var input = document.getElementById("selected_files")
      if(input) { // if user has already checked some cases just modify the cases to be deleted
        input.value = values;
      } else { // otherwise create a new hidden input element
        var theForm = document.getElementById("delete_modal");
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_files';
        input.id = 'selected_files';
        input.value = values;
        theForm.appendChild(input);
      }

      var input = document.getElementById("selected_files_zip")
      if(input) { // if user has already checked some cases just modify the cases to be deleted
        input.value = values;
      } else { // otherwise create a new hidden input element
        // add selected files to Zip form
    	var theForm = document.getElementById("zipform");
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_files_zip';
        input.id = 'selected_files_zip';
        input.value = values;
        theForm.appendChild(input);
      }

      var input = document.getElementById("selected_files_mod")
      if(input) { // if user has already checked some cases just modify the cases to be deleted
        input.value = values;
      } else { // otherwise create a new hidden input element
        // add selected files to Scale form
    	var theForm = document.getElementById("modform");
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_files_mod';
        input.id = 'selected_files_mod';
        input.value = values;
        theForm.appendChild(input);
      }

    }
</script>

%include('navbar')
%include('navactions')


<div class="row">

	<div class="hidden-xs col-md-4">
		<form id="search_form" role="form" action="/files">
			<input type="hidden" name="cid" value="{{cid}}"/>
			<input type="hidden" name="app" value="{{app}}"/>
			<input name="q" type="text" value="{{q}}" class="form-control input-lg"
			       placeholder="File filter... e.g. *.dat">
		</form>
	</div>

	<div class="btn-group col-xs-12 col-md-8" id="actions" style="display:none">

	    <button id="delete_button" type="button" class="btn-group btn btn-danger" data-toggle="modal" data-target="#dModal"><span class="glyphicon glyphicon-trash"></span> Delete</button>

        <button id="" type="button" class="btn-group btn btn-default" data-toggle="modal" data-target="#modModal"><span class="glyphicon glyphicon-scale"></span> Modify</button>

	    <form id="zipform" class="btn-group" method="post" action="/files/zip_selected">
	    	<input type="hidden" name="app" value="{{app}}">
	    	<input type="hidden" name="cid" value="{{cid}}">
	    	<input type="hidden" name="selected_files">
	    	<button id="zip_button" type="submit" class="btn btn-warning"><span class="glyphicon glyphicon-compressed"></span> Zip</button>
	    </form>

	</div>

</div>


<table id="clickable" class="table table-striped">
	<tr>
		<th><input type="checkbox" onchange="toggle(this); toggle_delete_button_visibility()"></th>
		<th>Filename</th>
		<th>Size (Bytes)</th>
		<th>Timestamp</th>
	</tr>
	% import os, time
	% binary_extensions = ['.bz2', '.gz', '.xz', '.zip']
	% image_extensions = ['.png', '.gif', '.jpg', '.svg']
	% for file in files:
		<tr>
		<td><input type="checkbox" name="selected_files" value="{{file}}:" onchange="toggle_delete_button_visibility()"></td>
		<td>
		% _, ext = os.path.splitext(file)
		% stat = os.stat(os.path.join(path,file))
		% if os.path.isdir(os.path.join(path,file)):
			<a href="/files?app={{app}}&cid={{cid}}&path={{path}}/{{file}}">{{file}}/</a>
		% elif ext in binary_extensions:
			<a href="{{path}}/{{file}}">{{file}}</a>
		% elif ext in image_extensions:
			<a href="{{path}}/{{file}}"><img src="{{path}}/{{file}}" width="100"><br> {{file}} </a> </td>
		% else:
			<a href="/more?app={{app}}&cid={{cid}}&filepath={{path}}/{{file}}">{{file}}</a>
		% end
		</td>
		<td>{{stat.st_size}} </td>
		<td>{{time.strftime("%c",time.localtime(stat.st_mtime))}}</td>
		<!-- <td><span class="glyphicon glyphicon-remove"></span></td> -->
		</tr>
	% end
</table>

<!-- Delete Modal -->
<div class="modal fade" id="dModal" tabindex="-1" role="dialog"
     aria-labelledby="deleteModal">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <form id="delete_modal" class="form-horizontal" method="post" action="/files/delete_selected">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" id="deleteModal">Delete Selected Files?</h4>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-danger center-block">Delete</button>
                    <input type="hidden" name="app" value="{{app}}"/>
                    <input type="hidden" name="cid" value="{{cid}}"/>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Modify Modal -->
<div class="modal fade" id="modModal" tabindex="-1" role="dialog"
     aria-labelledby="modModal">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <form id="modform" class="form-horizontal" method="post">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title">Modify Selected Files?</h4>
                </div>
                <div class="modal-footer">
                    <div class="row">
                        <div class="col-xs-6">
                            <input type="text" name="factor" class="input-lg form-control" placeholder="factor, e.g. 1000" />
                            <input type="text" name="columns" class="input-lg form-control" placeholder="columns, e.g. 5:6" />
                        </div>
                        <div class="btn-group col-xs-6">
                            <button formaction="/files/modify/add" type="submit" class="btn btn-default"><font size="+2">&plus;</font></button>
                            <button formaction="/files/modify/sub" type="submit" class="btn btn-default"><font size="+2">&minus;</font></button>
                            <button formaction="/files/modify/mul" type="submit" class="btn btn-default"><font size="+2">&times;</font></button>
                            <button formaction="/files/modify/div" type="submit" class="btn btn-default"><font size="+2">&divide;</font></button>
                        </div>
                    </div>
                    <input type="hidden" name="app" value="{{app}}"/>
                    <input type="hidden" name="cid" value="{{cid}}"/>
                </div>
            </form>
        </div>
    </div>
</div>

%include('footer')
