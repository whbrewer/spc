<style type="text/css"> a {text-decoration: none} </style>

<b>Available plots</b>
%for row in rows:
    :: <a style="{text-decoration: none}" href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">{{row['plots']['title']}}</a> 
%end

<div class="container-fluid">
    <div class="row">
    <h3 align="left">{{title}} ({{cid}})</h3>
    <div class="btn-group align-right">
        <form class="btn-group" action="/more" method="get">
            <button class="btn btn-default">Show Data</button>
            <input type="hidden" name="cid" value="{{cid}}">
            <input type="hidden" name="app" value="{{app}}">
            <input type="hidden" name="filepath" value="{{plotpath}}">
        </form>
        <form class="btn-group" action="/plots/edit" method="get">
            <button class="btn btn-default">Edit Plots</button>
            <input type="hidden" name="cid" value="{{cid}}">
            <input type="hidden" name="app" value="{{app}}">
        </form>
        <form class="btn-group" action="/plots/datasource/{{pltid}}" method="get">
            <button class="btn btn-default">Edit Datasource</button>
            <input type="hidden" name="cid" value="{{cid}}">
            <input type="hidden" name="app" value="{{app}}">
        </form>
    </div>
    </div>
</div>
