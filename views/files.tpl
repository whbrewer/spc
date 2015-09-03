%include('header', title='Menu')

<body>
<style>
  a { font-size: 120% }
</style>

%include('navbar')
%include('navactions')

<table class="table table-striped">
	<tr>
		<th>Filename</th>
		<th>Size (Bytes)</th>
		<th>Timestamp</th>
	</tr>
	% import os, time
	% binary_extensions = ['.bz2','.gz','.xz','.zip']
	% image_extensions = ['.png','.gif','.jpg']
	% for file in files:
		<tr>
		% _, ext = os.path.splitext(file)
		% stat = os.stat(os.path.join(path,file))
		% if os.path.isdir(os.path.join(path,file)):
			<td> <a href="/files?app={{app}}&cid={{cid}}&path={{path}}/{{file}}">{{file}}/</a> </td>
		% elif ext in binary_extensions:
			<td> <a href="{{path}}/{{file}}">{{file}}</a> </td>
		% elif ext in image_extensions:
			<td> <a href="{{path}}/{{file}}"><img src="{{path}}/{{file}}" width="100"></a> </td>
		% else:
			<td> <a href="/more?app='{{app}}&cid={{cid}}&filepath={{path}}/{{file}}">{{file}}</a></td>
		% end
		<td>{{stat.st_size}} </td>
		<td>{{time.strftime("%c",time.localtime(stat.st_mtime))}}</td>
		<!-- <td><span class="glyphicon glyphicon-remove"></span></td> -->
		</tr>
	% end
</table>

%include('footer')
