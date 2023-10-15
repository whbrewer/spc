%include('navactions')

<div class="container-fluid">
    <div class="row">
        <div class="col-sm-8">
            <h3 class="text-center">{{plot_title}}</h3>
            <div id="myplot" style="height:calc(100vh - 280px)"></div> <br>
        </div>
        <div class="col-sm-4 sidebar">
            <h4>Available Plots:</h4>
            <ul class="nav nav-sidebar">
                %i = 0
                %for row in rows:
                    % i += 1
                    % if defined('jid'):
                        <li> <a style="text-decoration:none" href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}&jid={{jid}}"><sup>{{i}}</sup> {{row['plots']['title']}}</a> </li>
                    % else:
                        <li> <a style="text-decoration:none" href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}"><sup>{{i}}</sup> {{row['plots']['title']}}</a> </li>
                    % end
                %end
            </ul>
        </div>
    </div>

    <div class="row">
        <div class="col-sm-12">
            <div>
                <h4>Summary Statistics:</h4>
                <pre>
<!--         -->{{!stats}}
                </pre>
            </div>
        </div>
    </div>
</div>
