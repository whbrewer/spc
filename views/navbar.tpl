<div class="navbar">

<form id="plotform" action="/list" method="post">
<input type="text" class="cid" name="cid" id="cid" value="{{cid}}"/>
<input type="submit" formaction="/{{app}}/start" class="start" value="start"/>
<input type="submit" formaction="/{{app}}/{{cid}}/plot" class="plot" value="plot"/>
<input type="submit" formaction="/{{app}}/list" class="list" value="list"/>
<input type="submit" formaction="/{{app}}/{{cid}}/output" class="output" value="output"/>
</form>

</div>

