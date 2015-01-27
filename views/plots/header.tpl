%include('navactions')

<style type="text/css"> a {text-decoration: none} </style>

<b>Available plots</b>
%for row in rows:
    :: <a style="{text-decoration: none}" href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">{{row['plots']['title']}}</a> 
%end

<!--<h1 align=center>Available plots for {{app}} app ({{cid}})</h1>-->
<table width=600>
<tr>
    <td>
        <h3 align="left">{{title}} ({{cid}})</h3>
    </td>
    <td align="right">
        <div align="right">
            <form method="get" action="/more">
                <input type="hidden" name="app" value="{{app}}">
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="hidden" name="filepath" value="{{plotpath}}">
                <input type="submit" value="Show Data">
            </form>
        </div>
    </td>
    <td>
            <form method="get" action="/plots/edit">
                <input type="hidden" name="app" value="{{app}}">
                <input type="hidden" name="cid" value="{{cid}}">
                <input type="submit" value="Edit Plots">
            </form>
    </td>
</tr>
</table>
