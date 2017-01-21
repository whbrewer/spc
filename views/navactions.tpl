
<div id="navaction" class="container-fluid navbar navbar-inverse navbar-fixed-bottom" style="padding-left:0px;padding-top:10px">

    <div class="visible-xs" style="height:10px"></div>

    <div class="col-xs-12">
        <div class="btn-group">
            <form class="btn-group" action="/start" method="get">
                <button class="btn btn-success">
                    <span class="glyphicon glyphicon-repeat"></span> Restart
                </button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>

            %if defined('jid'):
                %if jid > 0:
                    <form class="btn-group hidden-xs" role="form" action="/jobs/stop" method="post">
                        <input type="hidden" name="cid" value="{{cid}}">
                        <input type="hidden" name="app" value="{{app}}">
                        <input type="hidden" name="jid" value="{{jid}}">
                        <button class="btn btn-warning"><span class="glyphicon glyphicon-stop"></span> Stop</button>
                    </form>  

                    <button type="button" class="btn btn-danger hidden-xs" 
                            data-toggle="modal" data-target="#dModal">
                            <span class="glyphicon glyphicon-trash"></span> Delete
                    </button>
                %end
            %end

            <form class="btn-group hidden-xs" action="/case" method="get">
                <button class="btn btn-default"><span class="glyphicon glyphicon-hourglass">
                </span> Monitor</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>

            <form class="btn-group" action="/plot/0" method="get">
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
                <button class="btn btn-default">
                    <span class="glyphicon glyphicon-stats"></span> Plot
                </button>
            </form>

            %if defined('plotpath'):  
                <form class="btn-group" role="form" action="/more" method="get">
                    <input type="hidden" name="cid" value="{{cid}}">
                    <input type="hidden" name="app" value="{{app}}">
                    <input type="hidden" name="filepath" value="{{plotpath}}">
                    <button class="btn btn-warning hidden-xs"><span class="glyphicon glyphicon-list-alt"></span> Data</button>
                </form>    
            %end  
            
            <form class="btn-group" method="get" action="/output?cid={{cid}}&app={{app}}">
                <button class="btn btn-default"><span class="glyphicon glyphicon-file"></span> Output</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>       

            <div class="btn-group dropdown hidden-xs">

                <button class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                        <span class="glyphicon glyphicon-folder-open"></span> Files <span class="glyphicon glyphicon-chevron-up"></span>
                </button>

                <ul class="dropdown-menu" style="background-color:#404040;padding:10px">
                    <li> 
                        <form class="btn-group" action="/files" method="get">
                            <button class="btn btn-default" style="width:200px">
                                <span class="glyphicon glyphicon-folder-open"></span> Browse Files</span>
                            </button>
                            <input type="hidden" name="cid" value="{{cid}}">
                            <input type="hidden" name="app" value="{{app}}">
                        </form>
                    </li>

                    <li>
                        <form class="btn-group" action="/zipcase" method="get">
                            <button class="btn btn-default" style="width:200px">
                                <span class="glyphicon glyphicon-cloud-download"></span> Download
                            </button>
                            <input type="hidden" name="cid" value="{{cid}}">
                            <input type="hidden" name="app" value="{{app}}">
                        </form>
                    </li>

                    <li>
                        <form class="btn-group" method="get" action="/inputs?cid={{cid}}&app={{app}}">
                            <button class="btn btn-default" style="width:200px">
                                <span class="glyphicon glyphicon-wrench"></span> Inputs</button>
                            <input type="hidden" name="cid" value="{{cid}}">
                            <input type="hidden" name="app" value="{{app}}">
                        </form>
                    </li>

                </ul>

            </div>

            <!-- <form class="btn-group hidden-xs hidden-sm" action="/zipget" method="get">
                <button class="btn btn-default">
                    <span class="glyphicon glyphicon-transfer"></span> Fetch</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form> -->

        </div>

        <span id="stats" class="navbar-brand navbar-right hidden-xs hidden-sm"></span>

    </div>
</div>

%if defined('jid'):
%if jid > 0: 
<!-- Delete Modal -->
<div class="modal fade" id="dModal" tabindex="-1" role="dialog" 
     aria-labelledby="deleteModal">
    <div class="modal-dialog" role="document">
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

%if defined('description'):
<!-- Label Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" 
     aria-labelledby="myModalLabel">
    <div class="modal-dialog" role="document">
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
                    <input type="hidden" name="jid" value="{{jid}}">
                    <input type="text" class="form-control" data-role="tagsinput"
                    name="description" value="{{description}}">
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-success center-block">Save changes</button>
                </div>
            </form>
        </div>
    </div>
</div>
%end
%end
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
        $.get('stats/mem', function(data) {
            var obj = $.parseJSON(data)
            $('#stats').html("<tt>CPU: " + obj.cpu + "% MEM: " + obj.mem + "%</tt>");  
            setTimeout(pollStats,5000);
        });
    }

    if ($(window).width() >= 768) {
        pollStats()
    }

});
</script>




