%style = "#navaction { display: none }"
%rebase('base.tpl', style=style)

%if defined('status'):
    Status: {{status}}
%end

%include("navactions")

<pre>
{{!contents}}
</pre>
<span>file: {{fn}}</span>

<script>
$(function() { $('#navaction').fadeIn() })
</script>
