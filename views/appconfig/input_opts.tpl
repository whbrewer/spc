<select class="form-control" style="width:auto" name="input_format">
%opts = {'namelist': 'namelist.input', 'ini': 'INI file', 'xml': 'XML file', 'json': 'JSON file', 'yaml': 'YAML file', 'toml': 'TOML file'}
%for key, value in opts.iteritems():
    %if key == input_format:
	<option selected value="{{key}}">{{value}}
    %else:
	<option value="{{key}}">{{value}}
    %end
%end
</select>
