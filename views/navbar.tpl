<nav id="navbar" class="navbar navbar-inverse navbar-fixed-top" style="white-space:nowrap" role="navigation">

<form class="navbar-form">
<div class="container-fluid">
    <div class="row" style="white-space:nowrap">
        <div class="navbar-left">
            <div class="btn-group">
                <button type="submit" class="btn btn-default" formaction="/myapps">
                    <span class="glyphicon glyphicon-th-large"></span> Apps </button>
                <button type="submit" class="btn btn-default" formaction="/jobs">
                    <span class="glyphicon glyphicon-tasks"></span> Jobs </button>
                <button type="submit" class="btn btn-default hidden-xs" formaction="/jobs/shared">
                    <span class="glyphicon glyphicon-pushpin"></span> Shared </button>
                <button type="submit" class="btn btn-default" formaction="/chat">
                    <span class="glyphicon glyphicon-comment"></span> Chat 
                    <span class="badge" style="background-color:tomato" id="unread_messages"></span>
                </button>
                %if defined('app'):
                    %if app != '':
                        <button type="submit" class="btn btn-success hidden-xs" 
                                formaction="/start">
                            <span class="glyphicon glyphicon-play-circle"></span> Start </button>
                    %end
                %end
            </div>
        </div>

        <div class="hidden-xs hidden-sm">
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

            %if defined('status'):
                <span class="navbar-brand">{{!status}}</span>
            %end
        </div>

        %if True:

        <div class="navbar-right hidden-xs" style="margin-right: 5px;">
            %if defined('user'):
                <label class="navbar-brand hidden-sm">{{user}}</label>
            %end
            <div class="btn-group">
                <a data-toggle="dropdown" class="btn btn-default dropdown-toggle">
                    <span class="glyphicon glyphicon-menu-hamburger"></span></a>

                <ul class="dropdown-menu" role="menu">
                    <li> <a href="/account">Account</a> </li>
                    <li class="divider"> </li>
                    <li> <a href="/aws">AWS</a>
                    <li> <a href="/docker">Docker</a>
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

<script>
$(document).ready(function () {
    setInterval("check_for_messages()", 5000);
});

function check_for_messages() {
    $.get( "/chat/unread_messages", function( data ) {
        if (eval(data) > 0) {
            $("#unread_messages").text(data)
        } else {
            $("#unread_messages").text("")
        }
    });
}
</script>

</nav>



