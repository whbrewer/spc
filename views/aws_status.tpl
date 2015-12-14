%include('header')
%include('navbar')

<h1>Status of EC2 machine</h1>

<pre>
%for key,value in astatus.iteritems():
    {{key}}: {{value}} 
%end
</pre>

%if astatus['state']=="stopped":
    <a href="/aws/start/{{aid}}">start machine</a>
%elif astatus['state']=="running":
    <fieldset>
    <center>
    <p> LINK: <a href="http://{{astatus['public_dns_name']}}:{{port}}/">http://{{astatus['public_dns_name']}}:{{port}}</a> </p>
    <form action="/zipget">
        <input type="text" size="35" name="zipkey">
        <input type="hidden" name="netloc" value="http://{{astatus['public_dns_name']}}:{{port}}">
        <input type="submit" value="get case">
    </form>
    <a href="/aws/stop/{{aid}}">stop machine</a>
    </center>
    </fieldset>
%end

%include('footer')
