%include('header')
%include('navbar')

<h1>Status of EC2 machine</h1>

<pre>
%for key,value in status.iteritems():
    {{key}}: {{value}} 
%end
</pre>

%if status['state']=="stopped":
    <a href="/aws/start/{{aid}}">start</a>
%elif status['state']=="running":
    <p> LINK: <a href="http://{{status['public_dns_name']}}:8081/">http://{{status['public_dns_name']}}:8081</a> </p>
    <a href="/aws/stop/{{aid}}">stop</a>
%end

%include('footer')
