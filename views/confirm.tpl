%rebase('base.tpl')

<div class="container-fluid">
<div class="col-xs-12" style="height:5px"></div>

<div class="alert-info text-center">
    <em>Wrote parameters to input file. Click Execute to start simulation.</em>
</div>

<form class="form-horizontal" action="/execute" method="post">

    <div style="height:5px"></div>

    <div class="form-group">
        <div class="col-xs-12 col-sm-2">
            <button type="submit" class="btn btn-success"> <!-- pull-right -->
                Execute <em class="glyphicon glyphicon-play"></em>
            </button>
        </div>

        %if nap > 1:
            <input type="hidden" name="np" value="{{nap}}">
        %else:
            <input type="hidden" name="np" value="1">
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
                <option value="2147483647">Unlimited</option>
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
