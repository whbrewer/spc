%include('header')
%include('navbar')

<script>
    function start_ec2() {
        $.post("/aws/{{aid}}")
        $("#start_button").prop('disabled', true)
        $("#loading-indicator").show()
        $(document).bind("ajaxComplete", function(){
            location.reload(true)
        })
    }
    function stop_ec2() {
        $.ajax({ url: "/aws/{{aid}}", type: "DELETE" })
        $("#loading-indicator").show();
        $("#stop_button").prop('disabled', true);
        $(document).bind("ajaxComplete", function(){
            location.reload(true)
        })
    } 
</script>

<h1>Status of EC2 machine</h1>

<pre>
%for key,value in astatus.iteritems():
    {{key}}: {{value}} 
%end
</pre>

<fieldset>
<center>

%if astatus['state']=="stopped":
    <button class="btn btn-success" onclick="start_ec2()" id="start_button"> <span class="glyphicon glyphicon-play"></span> start machine</button>

%elif astatus['state']=="running":

    <p> LINK: <a target="_blank" href="http://{{astatus['public_dns_name']}}:{{port}}/">http://{{astatus['public_dns_name']}}:{{port}}</a> <span class="glyphicon glyphicon-new-window"></span></p>

    <div class="row">
        <div class="col-xs-12 col-sm-offset-2 col-sm-8">
            <form class="form-horizontal" action="/zipget">
                <div class="input-group">
                    <input type="text" class="form-control input-lg" name="cid">
                    <span class="input-group-btn">
                        <input type="submit" class="btn btn-default" value="get case">
                    </span>
                    <input type="hidden" name="app" value="mendel">
                    <input type="hidden" name="url" value="http://{{astatus['public_dns_name']}}:{{port}}">
                </div>
            </form>
        </div>
    </div>

    <div class="col-xs-12 center-block">
        <button class="btn btn-danger" onclick="stop_ec2()" id="stop_button"> <span class="glyphicon glyphicon-stop"></span> stop machine</button>
    </div>

%else:
    <meta http-equiv="refresh" content="2">
%end

<img src="/static/images/loading.gif" id="loading-indicator" style="display:none" />

</center>
</fieldset>

%include('footer')
