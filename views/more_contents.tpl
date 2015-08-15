%if defined('progress'):
	%if progress > 0:
		<div class="container-fluid">
			<div class="progress">
				<div class="progress-bar" role="progressbar" aria-valuenow="{{progress}}"
				 aria-valuemin="0" aria-valuemax="100" style="width:{{progress}}%">
				{{progress}}%
				</div>
			</div>
		</div>
	%end
%end

<div id="mydiv">
<pre>
{{!contents}}
</pre>
</div>
