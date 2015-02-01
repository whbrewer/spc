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

%if defined('app'):
{{app}}
%end
<form id="plotform" action="/start" method="get">

<!--
%if defined('cid'):
    <input type="text" class="cid" name="cid" id="cid" value="{{cid}}"/>
%else:
    <input type="text" class="cid" name="cid" id="cid"/>
%end
-->

<select name="app" onchange="this.form.submit()">
    <option>app...
    %for app in apps:
       <option value="{{app}}">{{app}}
    %end
</select>
<!-- <input type="submit" formaction="/apps" class="submit apps" value="apps"/> -->
<input type="submit" formaction="/jobs" class="submit jobs" value="myjobs"/>
<input type="submit" formaction="/wall" class="submit wall" value="wall"/>
%if defined('app'):
<input type="submit" formaction="/plots/edit" class="submit plot" value="plots"/>
%end
</form> 

<!--<img class="clear" style="cursor: pointer" src="/static/images/clear_left.png" onclick="document.getElementById('cid').value=''"/>-->

</div>

