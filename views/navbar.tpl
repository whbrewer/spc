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

<form id="plotform" action="/start" method="get">

<!-- <input type="submit" formaction="/apps" class="submit apps" value="apps"/> -->
<input type="submit" formaction="/start" class="submit start" value="start"/>
<input type="submit" formaction="/jobs" class="submit jobs" value="myjobs"/>
<input type="submit" formaction="/wall" class="submit wall" value="wall"/>

%if defined('app'):
<input type="submit" formaction="/plots/edit" class="submit plot" value="plots"/>
<select class="submit apps" name="app" onchange="this.form.submit()">
    %for a in apps:
       %if a == app:
           <option selected value="{{a}}">{{a}}
       %else:
           <option value="{{a}}">{{a}}
       %end
    %end
</select>
%end

</form> 

</div>

