<div class="navbar">
<!--
<a href="/apps/show/name" border=0>
<img align="left" height="43" src="/static/images/scipaas.png"/>
</a>
-->
<form id="plotform" action="/{{app}}" method="get">
<input type="text" class="cid" name="cid" id="cid" value="{{cid}}"/>
<input type="hidden" name="app" id="app" value="{{app}}"/>
<input type="submit" formaction="/start" class="submit start" value="start"/>
<input type="submit" formaction="/inputs" class="submit inputs" value="inputs"/>
<input type="submit" formaction="/output" class="submit output" value="output"/>
<input type="submit" formaction="/plots" class="submit plot" value="plot"/>
<input type="submit" formaction="/jobs" class="submit jobs" value="myjobs"/>
<input type="submit" formaction="/wall" class="submit wall" value="wall"/>
</form>

</div>

