%include('header', title='Menu')

<body>
<style>
  a { font-size: 120% }
</style>

%include('navbar')
%include('navactions')

<div class="hidden-xs col-md-4">
	<form id="search_form" role="form" action="/files">
		<input type="hidden" name="cid" value="{{cid}}"/>
		<input type="hidden" name="app" value="{{app}}"/>
		<input name="q" type="text" value="{{q}}" class="form-control input-lg" 
		       placeholder="File filter... e.g. *.dat">
	</form>
</div>

<table id="clickable" class="table table-striped">
	<tr>
		<th>Filename</th>
		<th>Size (Bytes)</th>
		<th>Timestamp</th>
	</tr>
	% import os, time
	% binary_extensions = ['.bz2','.gz','.xz','.zip']
	% image_extensions = ['.png','.gif','.jpg']
	% for file in files:
		<tr><td>
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

<script>
$(document).ready(function() {
    $('#clickable tr').click(function(e) {
        var href = $(this).find("a").attr("href");
        if(href) { window.location = href; }
        e.stopPropagation();
    });
});
</script>

%include('footer')
