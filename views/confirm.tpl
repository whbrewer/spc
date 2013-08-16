%include header title='confirm'
<body onload="init()">
%include navbar

<h1>Execute simulation:</h1>

<p>wrote parameters file needed for simulation</p>
<p>click "execute" to start the simulation</p>

<form action="/{{app}}/{{cid}}/execute" method="post" onclick="showImage()">
<input class="start" type="submit" value="execute"/>
</form>

<img id="loadingImage" src="/static/ajax_loader.gif" style="visibility:hidden"/> 

%include footer
