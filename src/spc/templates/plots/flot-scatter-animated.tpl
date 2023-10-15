% rebase('plots/flot-base.tpl')

<div>
   <!--
   <img id="canvasImg" alt="Right click to save me!">
   <p align="right">
       <button type="button" onclick="showcanvas()">Show canvas</button>
       <button type="button" onclick="showimage()">Show image</button>
       <button type="button" onclick="download()">Download image</button>
   </p>
   -->

   <script id="source">
      function download()  {
          document.location.href=document.getElementById('canvasImg').src;
      }

      function showcanvas() {
          document.getElementById('canvasImg').style.display = "none";
          document.getElementById('myplot').style.display = "block";
      }
      function showimage() {
          document.getElementById('canvasImg').style.display = "block";
          document.getElementById('myplot').style.display = "none";
      }

      $(function () {
          %i=0
          %for d in data:
          %i+=1
              var d{{i}} = {{!d}};
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

          $(window).resize(function() {
             var plot = $.plot(placeholder, data, options);
          });

          var plot = $.plotAnimator(placeholder, data, options);

          // convert plot to image and display
          var canvas = plot.getCanvas();
          var image = canvas.toDataURL();

          // this line causes browser to download file instead of display
          //image = image.replace("image/png","image/octet-stream");
          //document.getElementById('canvasImg').src = image;
          //document.getElementById('canvasImg').style.display = "none";

          // this is python code related to saving images on the server side
          //http://stackoverflow.com/questions/6930050/howto-export-jquery-flot-graphs-as-images
          //in python, I can use base64.b64decode([chart data]) to get the image
          //https://github.com/RobberPhex/PyCI/blob/master/utils.py
          //https://github.com/andrefsp/pyflot/blob/master/README.rst
          // write to server -- this is Python!!
          //imgstr = re.search(r'base64,(.*)', image).group(1)
          //output = open('output.png', 'wb')
          //output.write(imgstr.decode('base64'))
          //output.close()
   });
   </script>

</div>
