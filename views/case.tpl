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

<div id="output" style="width:648px;height:200px;"></div>

<script>
function show(update_interval) {
    showOutput = function() {
       jQuery('#output').load('/{{app}}/{{cid}}/tail', function(){
          setTimeout(showOutput, update_interval);
          // slow down updates over time to relieve burden on server
          if (update_interval < 10000) {
              update_interval+=500;
          }
       })
    }
    //$("#selector").hide()
    showOutput();
}
show(1000);
</script>

%include('footer')
