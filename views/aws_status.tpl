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
    <fieldset>
    <p> LINK: <a href="http://{{status['public_dns_name']}}:8081/">http://{{status['public_dns_name']}}:8081</a> </p>
    <form action="/zipget">
        <input type="text" size="35" name="zipkey">
        <input type="hidden" name="netloc" value="http://{{status['public_dns_name']}}:8081">
        <input type="submit" value="get file">
    </form>
    <a href="/aws/stop/{{aid}}">stop machine</a>
    </fieldset>
%end

%include('footer')
