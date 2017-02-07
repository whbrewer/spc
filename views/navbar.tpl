<nav id="navbar" class="navbar navbar-inverse navbar-fixed-top" style="white-space:nowrap" role="navigation">

    <form class="navbar-form">

        <div class="container-fluid">
            <div class="row" style="white-space:nowrap">
                <div class="navbar-left">
                    <div class="btn-group">

                        <button data-step="3" data-intro="Once you've activated your app, click here... You can always get back to this home page by clicking here" type="submit" class="btn btn-default" formaction="/myapps"><span class="glyphicon glyphicon-th-large"></span> Apps </button>

                        <button data-step="4" data-intro="Whenever you run a simulation, you can find it here" type="submit" class="btn btn-default" formaction="/jobs"><span class="glyphicon glyphicon-tasks"></span> Jobs </button>

                        <button data-step="5" data-intro="You can find other user's shared runs here" type="submit" class="btn btn-default hidden-xs" formaction="/jobs/shared"><span class="glyphicon glyphicon-pushpin"></span> Shared <span class="badge" style="background-color:tomato" id="new_shared_jobs"></span></button>

                        <button data-step="6" data-intro="Group chats happen here" type="submit" class="btn btn-default" formaction="/chat">
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
                    %if defined('app') and defined('cid'):
                        %if app != '' and cid != '':
                            <a href="/static/apps/{{app}}/about.html" 
                                class="navbar-brand" data-toggle="modal" 
                                data-target="#footModal">{{app}} :: {{cid}}</a>              
                        %end
                    %elif defined('app'):
                        %if app != '':
                            <a href="/static/apps/{{app}}/about.html" 
                                class="navbar-brand" data-toggle="modal" 
                                data-target="#footModal">{{app}}</a>              
                        %end
                    %end    

                    %if defined('status'):
                        <span class="navbar-brand">{{!status}}</span>
                    %end

                    %if defined('description'):
                        <div class="hidden-md">
                            <a href="#" class="navbar-brand" style="width:250px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap" 
                               data-toggle="modal" data-target="#myModal">
                            <span class="glyphicon glyphicon-tag"></span> {{description}}</a>
                        </div>
                    %end
                </div>


                <div class="navbar-right hidden-xs" style="margin-right: 5px;">
                    %if defined('user'):
                        <a onclick="toggleChatBox()"><label class="navbar-brand hidden-sm">{{user}}</label></a>
                    %end
                    <div data-step="7" data-intro="Change your password or use advanced features here" class="btn-group">
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

            </div>
        </div>

    </form>

</nav>

<!-- <div style="position:fixed; bottom:0px; right:0px">
    <button class="btn btn-default" onclick="toggleChatBox()">
        <span class="glyphicon glyphicon-comment"></span>
    </button>
</div> -->

<script>
$(document).ready(function () {
    setInterval(checkForNotifications, 5000);
});

function checkForNotifications() {
    $.get( "/notifications", function( data ) {
        var obj = $.parseJSON(data)

        if (eval(obj.unread_messages) > 0) {
            if ( $( "#chat_page" ).length ) {
                location.reload()
            } else {
                $("#unread_messages").html(obj.unread_messages)
            }
        } else {
            $("#unread_messages").html("")
        }

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

function toggleChatBox() {
    id = "#chatbox"
    time = 250
    if($(id).is(':visible')) {
        $(id).hide(time)
    } else {
        $(id).show(time)
    }
}
</script>
