
<div id="navaction" class="container-fluid navbar navbar-default navbar-fixed-bottom" style="padding-left:0px; padding-top:10px; padding-bottom:10px; bottom:0px">

    <div class="visible-xs" style="height:10px"></div>

    <div class="col-xs-12">
        <div class="btn-group">
            <form class="btn-group" action="/jobs/new" method="get">
                <button class="btn btn-success">
                    <span class="glyphicon glyphicon-repeat"></span> Rerun
                </button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>

            %if defined('jid') and owner == user and not defined('plotpath'):
                %if jid > 0:
                    <form class="btn-group hidden-xs" action="/jobs/stop" method="post">
                        <input type="hidden" name="cid" value="{{cid}}">
                        <input type="hidden" name="app" value="{{app}}">
                        <input type="hidden" name="jid" value="{{jid}}">
                        <button class="btn btn-warning"><span class="glyphicon glyphicon-stop"></span> Stop</button>
                    </form>

                    <button type="button"
                            class="btn btn-danger hidden-xs hidden-sm hidden-md"
                            data-toggle="modal" data-target="#dModal">
                            <span class="glyphicon glyphicon-trash"></span> Delete
                    </button>
                %end
            %end

            <form class="btn-group hidden-xs" action="/case" method="get">
                <button class="btn btn-default"><span class="glyphicon glyphicon-hourglass">
                </span> Monitor</button>
                % if defined('jid'):
                   <input type="hidden" name="jid" value="{{jid}}">
                % end
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>

            <form class="btn-group" action="/plot/0" method="get">
                % if defined('jid'):
                   <input type="hidden" name="jid" value="{{jid}}">
                % end
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
                <button class="btn btn-default">
                    <span class="glyphicon glyphicon-stats"></span> Plot
                </button>
            </form>

            %if defined('plotpath'):
                <form class="btn-group hidden-xs" action="/more" method="get">
                    <input type="hidden" name="cid" value="{{cid}}">
                    <input type="hidden" name="app" value="{{app}}">
                    <input type="hidden" name="filepath" value="{{plotpath}}">
                    <button class="btn btn-warning"><span class="glyphicon glyphicon-list-alt"></span> Data</button>
                </form>
            %end

            <form class="btn-group" method="get" action="/output?cid={{cid}}&app={{app}}">
                <button class="btn btn-default hidden-xs hidden-sm hidden-md"><span class="glyphicon glyphicon-file"></span> Output</button>
                % if defined('jid'):
                   <input type="hidden" name="jid" value="{{jid}}">
                % end
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>

            <div class="btn-group dropdown hidden-xs">

                <button class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                    <span class="glyphicon glyphicon-folder-open"></span> Files <span class="glyphicon glyphicon-chevron-up"></span>
                </button>

                <ul class="dropdown-menu">

                    <li> <a href="/zipcase?cid={{cid}}&app={{app}}">Download</a> </li>

                    <li> <a href="/inputs?cid={{cid}}&app={{app}}">Inputs</a> </li>

                    <li> <a href="/output?cid={{cid}}&app={{app}}">Output</a> </li>

                    <li> <a href="/files?cid={{cid}}&app={{app}}">Files</a> </li>

                </ul>

            </div>

            <!-- <form class="btn-group hidden-xs hidden-sm" action="/zipget" method="get">
                <button class="btn btn-default">
                    <span class="glyphicon glyphicon-transfer"></span> Fetch</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form> -->

        </div>

        %if defined('cid'):
            &nbsp;&nbsp;&nbsp;
            <samp class="hidden-xs" style="color:#dfdfdf; font-size:x-large" ondblclick="document.execCommand('copy'); this.style.color='yellow'; this.style.transition='1s ease-in-out'">{{cid}}</samp>
        %end

        <span id="stats" class="navbar-right hidden-xs hidden-sm" style="position:relative;top:-10px"></span>

    </div>
</div>

%if defined('jid'):
%if jid > 0:
<!-- Delete Modal -->
<div class="modal fade" style="top:35%" id="dModal" tabindex="-1"
     aria-labelledby="deleteModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <form class="form-horizontal" method="post" action="/jobs/delete/{{jid}}">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" id="deleteModal">Delete Case {{cid}}?</h4>
                    <input type="hidden" name="app" value="{{app}}">
                    <input type="hidden" name="cid" value="{{cid}}">
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-danger center-block">Delete</button>
                </div>
            </form>
        </div>
    </div>
</div>
%end
%end

%if defined('description'):
<!-- Label Modal -->
<div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="myModalLabel">
    <div class="modal-dialog">
        <div class="modal-content">
            <form class="form-horizontal" method="post" action="/jobs/annotate">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" id="myModalLabel">Enter labels for case separated by commas</h4>
                </div>
                <div class="modal-body">
                    <input type="hidden" name="app" value="{{app}}">
                    <input type="hidden" name="cid" value="{{cid}}">
                    <input type="text" class="form-control input-lg" data-role="tagsinput"
                    name="description" placeholder="enter tag..." value="{{description}}">
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-success center-block">Save changes</button>
                </div>
            </form>
        </div>
    </div>
</div>
%end

<script>
// Dropdown Menu Fade
jQuery(document).ready(function(){
    $(".dropdown").hover(
        function() { $('.dropdown-menu', this).fadeIn("fast");
        },
        function() { $('.dropdown-menu', this).fadeOut("fast");
    });

    function pollStats(){
        $.get('/stats/mem', function(data) {
            var obj = $.parseJSON(data)
            $('#stats').html("<a class=\"navbar-brand\" href=\"/stats?cid={{cid}}&app={{app}}\"><samp>CPU: " + obj.cpu + "%<br>MEM: " + obj.mem + "%</samp></a>");
            setTimeout(pollStats,5000);
        });
    }

    if ($(window).width() >= 768) {
        pollStats()
    }

});
</script>
