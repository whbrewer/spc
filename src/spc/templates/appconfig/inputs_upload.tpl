%rebase('base.tpl')

<h3>Configure inputs: step 1 of 3</h3>

<br>

<h4>Upload input file</h4>

<div style="font-size:large; color=blue">
<p>Upload
%if input_format == "namelist":
    an input file named <b><samp>{{appname}}.in</samp></b>
%elif input_format == "ini":
    an input file named <b><samp>{{appname}}.ini</samp></b>
%elif input_format == "xml":
    an input file named <b><samp>{{appname}}.xml</samp></b>
%elif input_format == "yaml":
    an input file named <b><samp>{{appname}}.yaml</samp></b>
%elif input_format == "toml":
    an input file named <b><samp>{{appname}}.toml</samp></b>
%else:
    an input file named <b><samp>{{appname}}.json</samp></b>
%end
</p></div>

<div style="font-size:large">
<p>Your app must be able to read and parse a text input file with
the input parameters.</p>
</div>

<form action="/appconfig/inputs/parse" method="post" enctype="multipart/form-data">
  <span style="font-size:large">Select a file:</span>

  <input type="file" class="btn btn-default btn-file" name="upload"><br>
  <!-- see http://stackoverflow.com/questions/11235206/twitter-bootstrap-form-file-element-upload-busampon
  <span type="file" class="btn btn-default btn-file" name="upload">
  	Browse<input type="file">
  </span>
	-->
  	<br>
  <input type="hidden" name="appname" value="{{appname}}">
  <input type="hidden" name="input_format" value="{{input_format}}">
  <input type="submit" value="Next >>" class="btn btn-success"/>
</form>
