%rebase('base.tpl')

<div class="bs-callout bs-callout-danger">
<h2> ERROR: {{err}} </h2>
</div>

%if defined('traceback'):
<pre>
{{!traceback}}
</pre>
%end
