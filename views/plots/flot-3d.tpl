%include('header')
<body>
%include('navbar')
%include('plots/header')

<div style="display: none">
    <div id="flot-3d-data-json">{{!data_json}}</div>
    <div id="flot-3d-options-json">{{!options_json}}</div>
    <div id="flot-3d-z-data-json">{{!z_data_json}}</div>
    <div id="flot-3d-z-label-json">{{!z_label_json}}</div>
</div>

<script src="/static/js/flot/excanvas.min.js"></script>
<script src="/static/js/flot/jquery.min.js"></script>
<script src="/static/js/flot/jquery.flot.js"></script>
<script src="/static/js/flot/jquery.flot.axislabels.min.js"></script>
<script src="/static/js/flot/jquery.flot.selection.min.js"></script>
<script src="/static/js/flot/jquery.flot.fillbetween.min.js"></script>
<script src="/static/js/flot/jquery.flot.resize.min.js"></script>
<script src="/static/js/flot/jquery.flot.stack.min.js"></script>
<script src="/static/js/flot/jquery.flot.animator.min.js"></script>

<script src="/static/js/plots/flot_3d.js"></script>

%include('footer')
