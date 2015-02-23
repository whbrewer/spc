%include('header')
<body onload="init()">
%include('navbar')

<h1>Execute simulation:</h1>

<p>wrote parameters file needed for simulation</p>
<p>click "execute" to start the simulation</p>

<form action="/execute" method="post">
<!-- onclick="showImage()"> -->
    Number of processors to use:
    <select name="np">
        %for i in range(1,np+1):
            <option value="{{i}}">{{i}}
        %end
    </select>
    <input class="submit start" type="submit" value="execute"/>
    <input type="hidden" name="app" value="{{app}}">
    <input type="hidden" name="cid" value="{{cid}}">
</form>

<!-- <img id="loadingImage" src="/static/ajax_loader.gif" style="visibility:hidden"/> -->
<hr>
<pre>
{{!inputs}}
</pre>

%include('footer')
