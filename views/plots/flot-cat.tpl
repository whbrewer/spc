<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="en">
<head>
    %include('header')

    <link href="/static/css/flot.css" rel="stylesheet" type="text/css">
    <script src="/static/js/flot/jquery.min.js"></script>
    <script src="/static/js/flot/jquery.flot.min.js"></script>
    <script src="/static/js/flot/jquery.flot.categories.min.js"></script>

    <style>
       #myplot div.xAxis div.tickLabel
       {
           transform: rotate(-45deg);
           -ms-transform:rotate(-45deg); /* IE 9 */
           -moz-transform:rotate(-45deg); /* Firefox */
           -webkit-transform:rotate(-45deg); /* Safari and Chrome */
           -o-transform:rotate(-45deg); /* Opera */
           /*rotation-point:50% 50%;*/ /* CSS3 */
           /*rotation:270deg;*/ /* CSS3 */
       }
    </style>

    %include('plots/style')
</head>

<body>
%include('navbar')
%include('plots/plot_list')

<div>
   <script id="source">
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
