% rebase('plots/flot-base.tpl')

<div>
   <div id="myplot" style="width:600px;height:370px;"></div> 
   <script id="source" language="javascript" type="text/javascript"> 
      $(function () {
      var d1 = {{!data}};
      var data = [ { label: "deleterious", data: d1, 
                     color: "rgb(200,0,0)" } ];

      var options = {
         legend: { position: 'nw' },
         xaxis:  { axisLabel: 'Generations', axisLabelFontSizePixels: 12 },
         yaxis:  { axisLabel: 'Mutations', axisLabelOffset: -30, 
                   axisLabelFontSizePixels: 12 },
                   //axisLabelFontSizePixels: 12, max: 0.01 },
         grid:   { hoverable: true, clickable: true },
         selection: { mode: "xy" }
      };

      var placeholder = $("#myplot");

      //myplot = new plotter(placeholder, data, options)
      //myplot.showPlot();

      // attach an event handler directly to the plot
      placeholder.bind("plotselected", function (event, ranges) {
        $("#selection").text(ranges.xaxis.from.toFixed(1) + " to " + ranges.xaxis.to.toFixed(1));

        plot = $.plot(placeholder, data,
               $.extend(true, {}, options, {
                  xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },
                  yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to }
               }));
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

</div>
