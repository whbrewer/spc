<nav id="navbar" class="navbar navbar-inverse navbar-fixed-top" style="white-space:nowrap" role="navigation">

    <form class="navbar-form">

        <div class="container-fluid">
            <div class="row" style="white-space:nowrap">
                <div class="navbar-left">
                    <div class="btn-group">

                        <button type="submit" class="btn btn-default" formaction="/myapps"><span class="glyphicon glyphicon-th-large"></span> Apps </button>

                        <button type="submit" class="btn btn-default" formaction="/jobs"><span class="glyphicon glyphicon-tasks"></span> Jobs </button>

                        <button type="submit" class="btn btn-default hidden-xs" formaction="/jobs/shared"><span class="glyphicon glyphicon-pushpin"></span> Shared </button>

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
                    %if defined('app') and defined('cid'):
                        %if app != '' and cid != '':
                            <a href="/static/apps/{{app}}/about.html" 
                                class="navbar-brand" data-toggle="modal" 
                                data-target="#footModal">{{app}}/{{cid}}</a>              
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
                        <a class="navbar-brand" data-toggle="modal" data-target="#myModal">
                        {{description}}</a>
                    %end
                </div>


                <div class="navbar-right hidden-xs" style="margin-right: 5px;">
                    %if defined('user'):
                        <a onclick="toggleChatBox()"><label class="navbar-brand hidden-sm">{{user}}</label></a>
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

            </div>
        </div>

        %if defined('app'):
            <input type="hidden" name="app" value="{{app}}">
        %end

    </form>

</nav>

<!-- <div style="position:fixed; bottom:0px; right:0px">
    <button class="btn btn-default" onclick="toggleChatBox()">
        <span class="glyphicon glyphicon-comment"></span>
    </button>
</div> -->

<script>
$(document).ready(function () {
    setInterval(checkForMessages, 5000);
    //setInterval("checkForNewSharedCases()", 12000)
});

function checkForMessages() {
    $.get( "/chat/unread_messages", function( data ) {
        if (eval(data) > 0) {
            if ( $( "#inbox" ).length ) {
                location.reload()
            } else {
                $("#unread_messages").text(data)
            }
        } else {
            $("#unread_messages").text("")
        }
    });
}

// function checkForNewSharedCases() {
//     $.get( "/jobs/shared/update", function( data ) {
//         if (eval(data) > 0) {
//             $("#unread_messages").text(data)
//         } else {
//             $("#unread_messages").text("")
//         }
//     });
// }

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
