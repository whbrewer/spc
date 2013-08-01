%include header title='confirm'

<h1>Execute simulation:</h1>

<p>wrote parameters file needed for simulation</p>
<p>click to start the simulation</p>

<form action="/execute" method="post" onclick="showImage()">
<input class="start" type="submit" value="Execute">
</form>

<img id="loadingImage" src="/static/ajax_loader.gif" style="visibility:hidden"/> 

%include footer
