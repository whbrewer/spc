%include('header')
<script src="/static/js/flot/excanvas.js"></script> 
<script src="/static/js/flot/jquery.js"></script>
<script src="/static/js/flot/jquery.flot.js"></script>
<script src="/static/js/flot/jquery.flot.axislabels.js"></script>
<script src="/static/js/flot/jquery.flot.selection.js"></script>
<script src="/static/js/flot/jquery.flot.fillbetween.js"></script>
<!--<script src="/static/js/canvas2image.js"></script>-->

<body onload="init()">
%include('navbar')
%include('plots/header')

{{!base}}

%include('footer')
