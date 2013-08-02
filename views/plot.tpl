%include header title='Menu'
<script language="javascript" type="text/javascript" src="/static/flot/excanvas.pack.js"></script> 
<script language="javascript" type="text/javascript" src="/static/flot/jquery.js"></script>
<script language="javascript" type="text/javascript" src="/static/flot/jquery.flot.js"></script>
<script language="javascript" type="text/javascript" src="/static/flot/jquery.flot.axislabels.js"></script>
<script language="javascript" type="text/javascript" src="/static/flot/jquery.flot.selection.js"></script>
<script language="javascript" type="text/javascript" src="/static/flot/jquery.flot.fillbetween.js"></script>

<body onload="init()">
%include button_start
%include navbar

<h1>Plots</h1>

<div class="tab-page">

   <h2 class="tab">mutations</h2>

   <h3>1: Average mutations/individual (tapaws)</h3>
   <p><i>updated every generation</i></p>

   <div id="mutations" style="width:600px;height:370px;"></div> 
   <script id="source" language="javascript" type="text/javascript"> 
      $(function () {
      var d1 = [
[1, 1.0053E+01], [2, 1.9851E+01], [3, 3.0075E+01], [4, 3.9864E+01], [5, 4.9752E+01], [6, 5.9653E+01], [7, 6.9597E+01], [8, 7.9566E+01], [9, 8.9591E+01], [10, 9.9485E+01], ];var d2 = [[1, 1.0000E-03], [2, 1.0000E-03], [3, 2.0000E-03], [4, 3.0000E-03], [5, 8.0000E-03], [6, 9.0000E-03], [7, 7.0000E-03], [8, 4.0000E-03], [9, 3.0000E-03], [10, 6.0000E-03], ];var d3 = [[1, 0.0000E+00], [2, 0.0000E+00], [3, 0.0000E+00], [4, 0.0000E+00], [5, 0.0000E+00], [6, 0.0000E+00], [7, 0.0000E+00], [8, 0.0000E+00], [9, 0.0000E+00], [10, 0.0000E+00], ];      var data = [ { label: "deleterious", data: d1, color: "rgb(200,0,0)" },
                   { label: "favorable",   data: d2, color: "rgb(0,200,0)" },
                   { label: "neutrals",    data: d3, color: "rgb(0,0,200)" } ];

      var options = {
         legend: { position: 'nw' },
         xaxis:  { axisLabel: 'Generations', axisLabelFontSizePixels: 12 },
         yaxis:  { axisLabel: 'Mutations', axisLabelOffset: -30, 
                   axisLabelFontSizePixels: 12 },
         grid:   { hoverable: true, clickable: true },
         selection: { mode: "xy" }
      };

      var placeholder = $("#mutations");

      //myplot = new plotter(placeholder, data, options)
      //myplot.showPlot();

      // attach an event handler directly to the plot
      placeholder.bind("plotselected", function (event, ranges) {
        $("#selection").text(ranges.xaxis.from.toFixed(1) + " to " + ranges.xaxis.to.toFixed(1));

        var zoom = $("#zoom").attr("checked");

        if (zoom)
            plot = $.plot(placeholder, data,
                   $.extend(true, {}, options, {
                      xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },
                      yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to }
                   }));
        else 
           var plot = $.plot(placeholder, data, options);
      });

      placeholder.bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));
      });

      placeholder.dblclick(function() {
         var plot = $.plot(placeholder, data, options);
      });

      var plot = $.plot(placeholder, data, options);

   });
   </script>

   <form name="mutn_form" method="post" action="more.pl">
   <input type="hidden" name="case_id" value="tapaws">
   <input type="hidden" name="file_name" value="tapaws.000.hst">
   <input type="hidden" name="run_dir" value="/Library/WebServer/Documents/mendel_user_data">
   <input type="hidden" name="user_id" value="wes">
   <input type="submit" value="Data">
   </form>

</div>

%include footer
