%include('header')
%include('navbar')

%if defined('status'):
    Status: {{status}}
%end

%include("navactions")

<body>

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

<div id="output"></div>

<script>

$(function() {
    $('#navaction').hide()
    $('#navaction').fadeIn()
});

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
  show(2147483647) // don't page reload unless in Run or Queue state
% else:
  show(1000) // comment out if using websocket
% end
</script>

%include('footer')
