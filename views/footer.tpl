<div class="lfooter">
<a href="/apps/show/name">SCIPAAS</a> &bull; 
<a href="/logout">logout</a>
</div>

<div class="rfooter">

%if defined('app'):
    app:{{app}} 
%else:
    app:none
%end
&bull; 

%if defined('user'):
    user:{{user}} 
%else:
    user:none
%end
&bull; 

%if defined('cid'):
    cid:{{cid}}
%else:
    cid:none
%end

</div>
</body>
</html>
