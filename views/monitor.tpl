%include header title='Monitor'
<script language="javascript" type="text/javascript" src="/static/flot/jquery.js"></script>

<body onload="init()">
%include navbar

<div id="output" style="width:648px;height:200px;"></div>

<script language="Javascript" type="text/javascript">

showOutput = function(){
   jQuery('#output').load('/{{app}}/{{cid}}/tail', function(){
      setTimeout(showOutput, 1000);
   })
}

showOutput();

</script>
