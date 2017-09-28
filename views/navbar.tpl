<nav id="navbar" class="navbar navbar-default navbar-fixed-top" style="white-space:nowrap">

    <form class="navbar-form">

        <div class="container-fluid">
            <div class="row" style="white-space:nowrap">
                <div class="navbar-left">
                    <div class="btn-group">

                        <button data-step="3" data-intro="You can always get back to this page by clicking here" type="submit" class="btn btn-default" formaction="/myapps"><span class="glyphicon glyphicon-th-large"></span> Apps </button>

                        <button data-step="4" data-intro="Whenever you run a simulation, you can find the data here" type="submit" class="btn btn-default" formaction="/jobs"><span class="glyphicon glyphicon-tasks"></span> Jobs </button>

                        <button data-step="5" data-intro="You can find other user's shared runs here" type="submit" class="btn btn-default hidden-xs" formaction="/jobs/shared"><span class="glyphicon glyphicon-pushpin"></span> Shared <span class="badge" style="background-color:tomato" id="new_shared_jobs"></span></button>

                        %if defined('app'):
                            %if app != '':
                                <button data-step="6" data-intro="Click this at any time to start a new run..." type="submit" class="btn btn-warning hidden-xs"
                                        formaction="/jobs/new">
                                    <span class="glyphicon glyphicon-play-circle"></span> {{app}}</button>
                            %end
                        %end
                    </div>
                </div>

                <div class="hidden-xs hidden-sm">
                    %if defined('status'):
                        <span class="navbar-brand">{{!status}}</span>
                    %end

                    %if defined('description'):
                        <div class="hidden-md">
                            <a href="#" class="navbar-brand" style="width:250px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap"
                               data-toggle="modal" data-target="#myModal">
                            <span class="glyphicon glyphicon-tag"></span> {{!description}}</a>
                        </div>
                    %end
                </div>

                <div class="navbar-right hidden-xs" style="margin-right: 5px;">
                    %if defined('user'):
                        <a href="#" class="navbar-brand hidden-xs">{{user}}</a>
                    %end
                    <div data-step="7" data-intro="Change your password or use advanced features (e.g. AWS, Docker integrations) here" class="btn-group">
                        <a data-toggle="dropdown" class="btn btn-default dropdown-toggle">
                            <span class="glyphicon glyphicon-menu-hamburger"></span></a>

                        <ul class="dropdown-menu" role="menu">
                            <li> <a href="/account">Account</a> </li>
                            <li class="divider"> </li>
                            <li> <a href="/aws">AWS</a> </li>
                            <li> <a href="/docker">Docker</a> </li>
                            <li> <a href="/stats">Machine Stats</a> </li>
                            <li class="divider"> </li>
                            %if defined('user'):
                                %if user=="admin":
                                    <li> <a href="/admin/show_users">Admin</a> </li>
                                    %if defined('app'):
                                        % if app != '':
                                        <li> <a href="/app/{{app}}">Configure {{app}}</a> </li>
                                        %end
                                    %end
                                %end
                            %end
                            <li class="divider"> </li>
                            <li> <a href="/logout">Logout</a> </li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>

    </form>

</nav>

%include('alerts')

<script>
window.addEventListener('load', checkForNotifications);

function checkForNotifications() {
    $.get( "/notifications", function( data ) {
        var obj = $.parseJSON(data)

        if (eval(obj.new_shared_jobs) > 0) {
            $("#new_shared_jobs").html(obj.new_shared_jobs)
            if ( $( "#shared_page" ).length ) {
                location.reload()
            }
        } else {
            $("#new_shared_jobs").html("")
        }
    });
}

</script>
