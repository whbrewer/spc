<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
<!-- <nav class="navbar navbar-default navbar-static-top" role="navigation"> -->
<form class="navbar-form">
<div class="container-fluid">
    <div class="row">
        <div class="navbar-left"> 
            <div class="btn-group">
                <button type="submit" class="btn btn-default" formaction="/apps">
                    <span class="glyphicon glyphicon-th-large"></span> Apps </button>
                %if defined('app'):
                %if app != '':
                <button type="submit" class="btn btn-default" formaction="/start">
                    <span class="glyphicon glyphicon-play-circle"></span> Start </button>
                %end
                %end
                <button type="submit" class="btn btn-default" formaction="/jobs">
                    <span class="glyphicon glyphicon-tasks"></span> Jobs </button>
                <button type="submit" class="btn btn-default" formaction="/jobs/shared">
                    <span class="glyphicon glyphicon-pushpin"></span> Shared </button>
            </div>
        </div> 

        %if defined('app'):
            %if app != '':
                <a class="navbar-brand" href="/">
                    <a href="/static/apps/{{app}}/about.html" 
                        class="navbar-brand" data-toggle="modal" 
                        data-target="#footModal">app: {{app}}</a>              
                </a>
            %end
        %end    
            
        %if defined("cid"):
            %if cid != '':
                <span class="navbar-brand">case: {{cid}}</span>
            %end
        %end

        %if True:

        <div class="navbar-right" style="margin-right: 5px;">
            %if defined('user'):
                <label class="control-label">{{user}}</label>
            %end
            <div class="btn-group">
                <a data-toggle="dropdown" class="btn btn-default dropdown-toggle">
                    <span class="glyphicon glyphicon-menu-hamburger"></span></a>

                <ul class="dropdown-menu" role="menu">
                    <li> <a href="/account">Account</a> </li>
                    <li class="divider"> </li>
                    <li> <a href="/aws">AWS</a>
                    <!-- <li> <a href="/docker">Docker</a> -->
                    %if defined('user'):
                        %if user=="admin":
                            <li> <a href="/admin/show_users">Admin</a> </li>
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

