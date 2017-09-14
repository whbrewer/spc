<%
    styles = """
        <style>
        #navaction { display: none }
        </style>
    """
%>

%rebase('base.tpl', styles=styles)

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
