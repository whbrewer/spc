%include('header')
%include('navbar')

<h1>Status of EC2 machine</h1>

<pre>
%for key,value in status.iteritems():
    {{key}}: {{value}} 
%end
</pre>

%include('footer')
