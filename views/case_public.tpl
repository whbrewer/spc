%include('header')
%include('navbar')

%if defined('status'):
    Status: {{status}}
%end

%include("navactions")

<pre>
{{!contents}}
</pre>
<span>file is: {{fn}}</span>

%include('footer')
