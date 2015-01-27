%include('header')
<link href="/static/css/flot.css" rel="stylesheet" type="text/css">
<script language="javascript" type="text/javascript" src="/static/flot/jquery.js"></script>
<script language="javascript" type="text/javascript" src="/static/flot/jquery.flot.js"></script>
<script language="javascript" type="text/javascript" src="/static/flot/jquery.flot.categories.js"></script>

<body onload="init()">
%include('navbar')
%include('plots/header')

<div>
   <script id="source" language="javascript" type="text/javascript"> 
      $(function () {
      var data = {{!data}};

        $.plot("#placeholder", [ data ], {
            series: {
                bars: {
                    show: true,
                    barWidth: 1.0,
                    align: "center"
                }
            },
            xaxis: {
                mode: "categories",
                ticks: {{!ticks}},
                tickLength: 0
            }
        });

   });
   </script>

</div>

<body>

    <div id="content">

        <div class="demo-container">
            <div id="placeholder" class="demo-placeholder"></div>
        </div>

    </div>

</body>

%include('footer')
