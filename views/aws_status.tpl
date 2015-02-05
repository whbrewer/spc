%include('header')
%include('navbar')

<h1>Status of EC2 machine</h1>

<pre>
%for key,value in status.iteritems():
    {{key}}: {{value}} 
%end
</pre>

<p> <a href="http://{{status['public_dns_name']}}:8081/">http://{{status['public_dns_name']}}:8081</a> </p>

%include('footer')
