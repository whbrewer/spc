<script>
function checkCase() { 
    if(!document.getElementByID('cid').value) { 
       alert('case id missing'); 
       return False;
    } else {
       return True;
    }
}

</script>

<div class="navbar">
<!--
<a href="/apps/show/name" border=0>
<img align="left" height="43" src="/static/images/scipaas.png"/>
</a>
-->
<form id="plotform" action="/{{app}}" method="get">
%if defined('cid'):
    <input type="text" class="cid" name="cid" id="cid" value="{{cid}}"/>
%else:
    <input type="text" class="cid" name="cid" id="cid"/>
%end

%if defined('app'):
    <input type="hidden" name="app" id="app" value="{{app}}"/>
%else:
    <input type="hidden" name="app" id="app"/>
%end
<input type="submit" formaction="/start" class="submit start" value="start"/>
<input type="submit" formaction="/inputs" class="submit inputs" value="inputs" onclick="checkCase()" } />
<input type="submit" formaction="/output" class="submit output" value="output"/>
<input type="submit" formaction="/plots" class="submit plot" value="plot"/>
<input type="submit" formaction="/jobs" class="submit jobs" value="myjobs"/>
<input type="submit" formaction="/wall" class="submit wall" value="wall"/>
</form> 
<img class="clear" src="/static/images/clear_left.png" onclick="document.getElementById('cid').value=''"/>

</div>

