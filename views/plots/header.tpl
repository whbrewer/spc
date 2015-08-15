<style> 
    a {text-decoration: none} 
    .tickLabel  { font-size: 120% }
    .legend { font-size: 120% }
</style>

%include('navactions')

<body>
<div class="container-fluid">
    <div class="row">
        <div class="col-sm-8">
            <h3>{{title}}</h3>
            <div id="myplot" style="width:100%; height:60%;"></div> <br>
        </div>
        <div class="col-sm-4 sidebar">
            <h4>Available Plots:</h4>
            <ul class="nav nav-sidebar">
                %for row in rows:
                    <li> <a style="{text-decoration: none}" href="/plot/{{row['plots']['id']}}?app={{app}}&cid={{cid}}">{{row['plots']['title']}}</a> </li>
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




