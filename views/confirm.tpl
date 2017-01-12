%include('header')
<body onload="toggle_np_visibility()">
%include('navbar')

<script>
function toggle_np_visibility() {
    var par_system = document.getElementById("par_system").value

    if (par_system == "none") {
        document.getElementById("np").disabled = true
    } else {
        document.getElementById("np").disabled = false
    }
}
</script>

<div class="container-fluid">
<div class="col-xs-12" style="height:5px"></div>

<div align="center" class="alert-info">
    <em>Wrote parameters to input file. Click Execute to start simulation.</em>
</div>

<form class="form-horizontal" action="/execute" method="post">

    <div style="height:5px"></div>

    <div class="form-group">
        <div class="col-sm-1">
            <input type="hidden" name="np" value="1">
            <button type="submit" class="btn btn-success"> <!-- pull-right -->
                Execute <em class="glyphicon glyphicon-play"></em>
            </button>
        </div>

        %if np > 1:
            <!-- <label for="par_system" class="control-label col-xs-12 col-sm-2">Parallel:</label>
            <div class="col-xs-12 col-sm-2">
                <select class="form-control" name="par_system" id="par_system" onchange="toggle_np_visibility()">
                    <option value="none" selected>None</option>
                    <option value="mpich">MPICH</option>
                    <option value="openmp">OpenMP</option>
                    <option value="hadoop">Hadoop</option>
                    <option value="spark">Spark</option>
                </select>
            </div> -->

            <label for="np" class="control-label col-xs-12 col-sm-2"># Processors:</label>
            <div class="col-xs-12 col-sm-1">
                <select name="np" id="np" class="btn-group form-control" title="Number of processors to use">
                    %for i in range(1, np+1):
                        <option value="{{i}}">{{i}}</option>
                    %end
                </select>
            </div>
        %end

        <label for="walltime" class="control-label col-xs-12 col-sm-2">Max run time:</label>
        <div class="col-xs-12 col-sm-2">
            <select class="form-control" name="walltime" id="walltime">
                <option value="60">1 min<!-- GAE front-end --></option>
                <option value="300">5 min <!-- AWS Lambda --></option>
                <option value="600">10 min <!-- GAE back-end --></option>
                <option value="3600" selected>60 min <!-- iron.io --></option>
                <option value="43200">12 hrs</option>
                <option value="86400">24 hrs</option>
                <option value="259200">96 hrs</option>
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
