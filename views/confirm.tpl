%include('header')
<body onload="init()">
%include('navbar')

<h1>Execute simulation:</h1>

<p>wrote parameters file needed for simulation</p>
<p>click "execute" to start the simulation</p>

<form action="/execute" method="post">
    <input type="hidden" name="np" value="1">
<!-- onclick="showImage()"> -->
    <!--
    <p>Number of processors to use:
    <select name="np">
        %for i in range(1,np+1):
            <option value="{{i}}">{{i}}
        %end
    </select></p>
    -->
    
    <!-- use this for testing priority levels
    <p>Priority level:
    <select name="priority">
        <option value="0">0
        <option value="1">1
        <option value="2">2
    </select>
    </p>
    -->

    <!-- <div class="container-fluid">
        <div class="row">
            <div class="col-md-12"> -->
                <button type="submit" class="btn btn-success abs-bottom-right">
                    Execute <em class="glyphicon glyphicon-play"></em>
                </button>
<!--             </div>
        </div>
    </div> -->

    <!--<input class="submit start" type="submit" value="execute"/>-->
    <input type="hidden" name="app" value="{{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
</form>

<pre>
{{!inputs}}
</pre>

<!-- <img id="loadingImage" src="/static/ajax_loader.gif" style="visibility:hidden"/> -->

%include('footer')
