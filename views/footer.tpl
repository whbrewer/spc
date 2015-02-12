<div class="lfooter">
<a href="/">SCIPAAS</a> &bull; 
<a href="/apps">apps</a> &bull;
<a href="/account">account</a> &bull;
<a href="/aws">aws</a> &bull;
%if defined('user'):
    %if user=="admin":
        <a href="/admin/show_users">admin</a> &bull;
    %end
%end
<a href="/logout">logout</a> 
</div>

<div class="rfooter">

%if defined('user'):
    user:{{user}} 
%else:
    user:none
%end
&bull; 

%if defined('app'):
    app:{{app}} 
%else:
    app:none
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
