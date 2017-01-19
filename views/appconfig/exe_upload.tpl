%include("header")

<h3>Configure Executable: step 1 of 2</h3>

<br>

<h4>Upload Executable File</h4>

<font size="+1">

<p>Upload an executable file that is compatible to run on the host platform.</p>

</font>

<form action="/appconfig/exe/test" method="post" enctype="multipart/form-data">
  <font size="+1">Select a file:</font> 

  <input type="file" class="btn btn-default btn-file" name="upload"><br>
  <input type="hidden" name="appname" value="{{appname}}">
  <input type="submit" class="btn btn-success" value="Next >>"/>
</form>
</div>

%include('footer')
