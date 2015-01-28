% rebase('plots/flot-base.tpl')

<div>
   <div id="myplot" style="width:600px;height:370px;"></div> 
   <script id="source" language="javascript" type="text/javascript"> 
      $(function () {
      %i=0
      %for d in data:
      %i+=1
          var d{{i}} = {{d}};
      %end
      var data = [
          %if datadef:
              {{!datadef}}
          %else:
              %i=0
              %for d in data:
              %i+=1
                  { data: d{{i}} }, 
              %end
          %end
      ]; 

      var options = {
          %if options:
              {{ !options }}
          %else:
              legend: { position: 'nw' },
              xaxis:  { axisLabelFontSizePixels: 12 },
              yaxis:  { axisLabelOffset: -30, 
                        axisLabelFontSizePixels: 12 },
              grid:   { hoverable: true, clickable: true },
              selection: { mode: "xy" }
          %end
      };

      var placeholder = $("#myplot");

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
