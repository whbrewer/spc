<nav class="navbar navbar-default navbar-static-top" role="navigation">
<form class="navbar-form">
<div class="container-fluid">
    <a class="navbar-brand" href="/">
        %if defined('app') and defined('cid'):
            {{app}} {{cid}}
        %else:
            %if defined('app'):
                {{app}}
            %else:
                SciPaaS
            %end
        %end
    </a>
    <div class="row">
        <div class="navbar-left"> 
            <div class="btn-group">
                <input type="submit" class="btn btn-default" 
                       formaction="/apps" value="Apps"> 
                <input type="submit" class="btn btn-default"
                       formaction="/start" value="Start"> 
                <input type="submit" class="btn btn-default" 
                       formaction="/jobs" value="Jobs"> 
                <button type="submit" class="btn btn-default" formaction="/shared">
                     <span class="glyphicon glyphicon-star"></span>Favs </button>
            </div>
        </div>
%if False:
        <div class="navbar-right">
            <div class="btn-group">
                <a data-toggle="dropdown" class="btn btn-default dropdown-toggle">
                    %if defined('user'):
                        {{user}}
                    %else:
                        Options
                    %end
                    <span class="caret"></span>
                </a>
                <ul class="dropdown-menu" role="menu">
                    <li> <a href="/account">Account</a> </li>
                    <li class="divider"> </li>
                    <li> <a href="/aws">AWS</a>
                    <li> <a href="/docker">Docker</a>
                    <li class="disabled"> <a href="/admin">Admin</a></li>
                    %if defined('user'):
                        %if user=="admin":
                            <li> <a href="/admin/show_users">admin</a> </li>
                        %end
                    %end
                    <li class="divider"> </li>
                    <li> <a href="/logout">Logout</a> </li>
                </ul>
            </div>
        </div>
%end
    </div>
</div>

%if defined('app'):
    <input type="hidden" name="app" value="{{app}}">
%else:
    <input type="hidden" name="app" value="dna">
%end
</form>
</nav>

%if defined('status'):
<div align="center">
    <font color="red">
        STATUS: {{!status}}
    </font>
</div>
%end

<!--
<script>
    $(document).ready(function () {
        $('.dropdown-toggle').dropdown();
    });
</script>
-->
