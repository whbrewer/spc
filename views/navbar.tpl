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

<form id="plotform" action="/{{get('app','')}}" method="get">

<!--
%if defined('cid'):
    <input type="text" class="cid" name="cid" id="cid" value="{{cid}}"/>
%else:
    <input type="text" class="cid" name="cid" id="cid"/>
%end
-->

<input type="submit" formaction="/apps" class="submit apps" value="apps"/>
%if defined('app'):
<input type="hidden" name="app" id="app" value="{{app}}"/>
<input type="submit" formaction="/start" class="submit start" value="start"/>
%else:
    <input type="hidden" name="app" id="app"/>
%end
<input type="submit" formaction="/jobs" class="submit jobs" value="myjobs"/>
<input type="submit" formaction="/wall" class="submit wall" value="wall"/>
%if defined('app'):
<input type="submit" formaction="/plots/edit" class="submit plot" value="plots"/>
%end
</form> 

<!--<img class="clear" style="cursor: pointer" src="/static/images/clear_left.png" onclick="document.getElementById('cid').value=''"/>-->

</div>

