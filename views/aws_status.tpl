%include('header')
%include('navbar')

<h1>Status of EC2 machine</h1>

<pre>
%for key,value in astatus.iteritems():
    {{key}}: {{value}} 
%end
</pre>

%if astatus['state']=="stopped":
    <a class="btn btn-success" href="/aws/start/{{aid}}"><span class="glyphicon glyphicon-play"></span> start machine</a>

%elif astatus['state']=="running":
    <fieldset>
    <center>
    <p> LINK: <a target="_blank" href="http://{{astatus['public_dns_name']}}:{{port}}/">http://{{astatus['public_dns_name']}}:{{port}}</a> <span class="glyphicon glyphicon-new-window"></span></p>

    <form class="form-horizontal" action="/zipget">
        <div class="col-xs-offset-3 col-xs-6 col-xs-offset-3">
            <div class="input-group">
                <input type="text" class="form-control" size="35" name="cid">
                <span class="input-group-btn">
                    <input type="submit" class="btn btn-default" value="get case">
                </span>
                <input type="hidden" name="app" value="mendel">
                <input type="hidden" name="url" value="http://{{astatus['public_dns_name']}}:{{port}}">
            </div>
        </div>
    </form>
    <br><br>

    <a class="btn btn-danger" href="/aws/stop/{{aid}}"><span class="glyphicon glyphicon-stop"></span> stop machine</a>               

    </center>
    </fieldset>
%end

%include('footer')
