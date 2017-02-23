%include('header')
%include('navbar')

%if defined('status'):
    Status: {{status}}
%end

%include("navactions")

<pre>
{{!contents}}
</pre>
<span>file: {{fn}}</span>

<script>
$('#navaction').fadeIn();
</script>

%include('footer')
