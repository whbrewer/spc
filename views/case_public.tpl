%include('header')
%include('navbar')

<style>
#navaction { display: none }
</style>

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
%include('footer')
