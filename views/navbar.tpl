<div class="navbar">
<!--
<a href="/apps/show/name" border=0>
   <img align="right" height="43" src="/static/scipaas.png"/>
</a>
-->
<form id="plotform" action="/{{app}}" method="get">
<input type="text" class="cid" name="cid" id="cid" value="{{cid}}"/>
<input type="submit" formaction="/{{app}}/start" class="submit start" value="start"/>
<input type="submit" formaction="/{{app}}/inputs" class="submit inputs" value="inputs"/>
<input type="submit" formaction="/{{app}}/output" class="submit output" value="output"/>
<input type="submit" formaction="/{{app}}/plots" class="submit plot" value="plot"/>
<input type="submit" formaction="/jobs/{{app}}" class="submit jobs" value="myjobs"/>
<input type="submit" formaction="/wall/{{app}}" class="submit wall" value="wall"/>
</form>

</div>

