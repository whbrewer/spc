<div class="container-fluid">
    <div class="col-md-12">
        <div class="btn-group">
            <form class="btn-group" action="/start" method="get">
                <button class="btn btn-default">Restart</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>
            <form class="btn-group" action="/files" method="get">
                <button class="btn btn-default">Files</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>
            <button href="/inputs?cid={{cid}}&app={{app}}" type="button" 
                    class="btn btn-default" data-toggle="modal" 
                    data-target="#myModal">Inputs</button>
            <button href="/output?cid={{cid}}&app={{app}}" type="button" 
                    class="btn btn-default" data-toggle="modal" 
                    data-target="#myModal">Output</button>
            <!--
            <form class="btn-group" action="/zipcase" method="get">
                <button class="btn btn-default">Zip</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>
            -->
            <form class="btn-group" action="/plot/0" method="get">
                <button class="btn btn-default">Plot</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>
            %if defined('jid'):
                <form class="btn-group" method="post" action="/jobs/delete/{{jid}}">
                    <button class="btn btn-default" 
                     onclick="if(confirm('are you sure?')) return true; return false">Delete</button> 
                    <input type="hidden" name="cid" value="{{cid}}">
                    <input type="hidden" name="app" value="{{app}}">
                </form>
                <form class="btn-group" method="post" action="/shared">
                    <input type="hidden" name="app" value="{{app}}">
                    <input type="hidden" name="cid" value="{{cid}}">
                    <input type="hidden" name="jid" value="{{jid}}">
                    <button class="btn btn-default">Star</button>
                </form>
                <button type="button" class="btn btn-default" data-toggle="modal" 
                        data-target="#myModal">Annotate</button>
            %end
        </div>
    </div>
</div>

%if defined('jid'):
<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" 
     aria-labelledby="myModalLabel">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
            <form class="form-horizontal" method="post" action="/jobs/annotate">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"> 
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" id="myModalLabel">Enter label for case</h4>
                </div>
                <div class="modal-body">
                    <input type="hidden" name="app" value="{{app}}">
                    <input type="hidden" name="cid" value="{{cid}}">
                    <input type="hidden" name="jid" value="{{jid}}">
                    <input type="text" class="form-control" 
                    name="description" value="{{description}}">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Save changes</button>
                </div>
            </form>
        </div>
    </div>
</div>
%end


