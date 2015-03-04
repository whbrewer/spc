<div class="navbar">

<form id="plotform" action="/start" method="get">

<!-- <input type="submit" formaction="/apps" class="submit apps" value="apps"/> -->
<input type="submit" formaction="/jobs" class="submit jobs" value="my jobs"/>
<input type="submit" formaction="/shared" class="submit shared" value="shared"/>

%if defined('app'):
<input type="submit" formaction="/start" class="submit start" value="start"/>
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

%if defined('status'):
<div align="center">
    <font color="red">
        STATUS: {{!status}}
    </font>
</div>
%end
