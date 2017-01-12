%include('header')
%include('navbar')

%if defined('status'):
    Status: {{status}}
%end

%include("navactions")

<!--
<form>
<select id="selector" onchange="show(this.value)">
<option value="Show output every...">
<option value="500">500ms
<option value="1000">1s
<option value="5000">5s
<option value="10000">10s
<option value="30000">30s
<option value="60000">1m
<option value="10000000000">&infin;
</select>
</form>
-->


% if sched == "ws":
  <style>
    .preformatted {
      font-family: monospace;
      white-space: pre;
      display: block;
      padding: 9.5px;
      margin: 0 0 10px;
      margin-bottom: 55px;
      font-size: 13px;
      line-height: 1.42857143;
      color: #333;
      word-break: break-all;
      word-wrap: break-word;
      background-color: #f5f5f5;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  </style>
  <div id="output" class="preformatted"></div>
% else:
  <div id="output"></div>
% end

<!-- <form name="nl" role="form">
  <div class="input-group col-xs-6" style="width:300px; padding-left:15px">
  <span class="input-group-addon">Number of lines to display</span>
  <input class="form-control" type="number" id="num_lines" min="10" max="100" value="24">
</form> -->

<script>

num_lines = parseInt(window.innerHeight/25)

function show(update_interval) {
    showOutput = function() {
       url = '/{{app}}/{{cid}}/tail?num_lines='+num_lines
       jQuery('#output').load(url, function(){
          setTimeout(showOutput, update_interval);
          // slow down updates over time to relieve burden on server
          if (update_interval < 10000) {
              update_interval += 500;
          }
       })
    }
    //$("#selector").hide()
    showOutput();
} 

% if state == "C" or state == "X":
  show(2**31-1) // don't page reload unless in Run or Queue state
% elif not sched == "ws":
  show(1000) // comment out if using websocket
% end
</script>

%include('footer')
