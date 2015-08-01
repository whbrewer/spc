<style type="text/css"> a {text-decoration: none} </style>

<div align="center" class="container-fluid">
    <div class="row">
        <h3 align="center">{{title}} ({{cid}})</h3>
        <div class="btn-group align-center">
            <div class="btn-group">
                <a data-toggle="dropdown" class="btn btn-default dropdown-toggle">
                    Select Plot
                    <span class="caret"></span>
                </a>
                <ul class="dropdown-menu" role="menu">
                    %for row in rows:
                        <li> <a style="{text-decoration: none}" href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">{{row['plots']['title']}}</a> </li>
                    %end
                </ul>
            </div>
            <button href="/more?cid={{cid}}&app={{app}}&filepath={{plotpath}}" 
                    type="button" 
                    class="btn btn-default" data-toggle="modal" 
                    data-target="#myModal">Show Data</button>
            <form class="btn-group" action="/plots/edit" method="get">
                <button class="btn btn-default">Plot Defs</button>
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
            </form>
            <form class="btn-group" action="/plots/datasource/{{pltid}}" method="get">
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="app" value="{{app}}">
                <button class="btn btn-default">Datasource</button>
            </form>
        </div>
    </div>
</div>

<div class="bs-example">
    <div id="myModal" class="modal fade">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <!-- Content will be loaded here -->
            </div>
        </div>

    </div>
</div>
