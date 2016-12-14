%include('header')
<body>
%include('navbar')

<div class="container-fluid">
<div class="col-xs-12" style="height:5px"></div>

<div align="center" class="alert-info">
    <em>Wrote parameters to input file. Click Execute to start simulation.</em>
</div>

<form class="form-horizontal" action="/execute" method="post">

    <div style="height:5px"></div>

    <div class="form-group">
        <div class="col-xs-6">
            %if np > 1:
                <div class="btn-group">
                    <button type="submit" class="btn btn-success"> <!-- pull-right -->
                        Execute <em class="glyphicon glyphicon-play"></em>
                    </button>
                    <select name="np" class="btn-group form-control" style="width:auto" title="Number of processors to use">
                        %for i in range(1,np+1):
                            <option value="{{i}}">{{i}}
                        %end
                    </select>
                </div>
            %else:
                <input type="hidden" name="np" value="1">
                <button type="submit" class="btn btn-success"> <!-- pull-right -->
                    Execute <em class="glyphicon glyphicon-play"></em>
                </button>
            %end
        </div>

        <label for="walltime" class="control-label col-xs-3">Max run time:</label>
        <div class="col-xs-3">
            <select class="form-control" name="walltime" id="walltime">
                <option value="60">1 minute (GAE front-end)</option>
                <option value="300" selected>5 minutes (AWS Lambda)</option>
                <option value="600">10 minutes (GAE back-end)</option>
                <option value="3600">60 minutes (iron.io)</option>
                <option value="43200">12 hours</option>
                <option value="86400">24 hours</option>
                <option value="259200">96 hours</option>
            </select>
        </div>

    </div>

    <div style="height:5px"></div>

    <input type="hidden" name="app" value="{{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
    %if defined('desc'):
    	<input type="hidden" name="desc" value="{{desc}}">
    %else:
    	<input type="hidden" name="desc" value="None">
    %end

<pre>
{{!inputs}}
</pre>

</form>

</div>

%include('footer')
