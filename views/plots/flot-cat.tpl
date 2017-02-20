%include('header')
<link href="/static/css/flot.css" rel="stylesheet" type="text/css">
<script language="javascript" type="text/javascript" src="/static/js/flot/jquery.min.js"></script>
<script language="javascript" type="text/javascript" src="/static/js/flot/jquery.flot.min.js"></script>
<script language="javascript" type="text/javascript" src="/static/js/flot/jquery.flot.categories.min.js"></script>

<body>
%include('navbar')
%include('plots/header')

<div>
   <script id="source" language="javascript" type="text/javascript">
      $(function () {

        var placeholder = "#myplot";

        var data = [{{!data[0]}}];

        var options = {
            %if options:
              {{ !options }}
            %else:
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
            %end
        };


        $(window).resize(function() {
           var plot = $.plot(placeholder, data, options);
        });

        $.plot(placeholder, data, options);
    });
   </script>

</div>

%include('footer')
