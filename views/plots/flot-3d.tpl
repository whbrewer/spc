<!DOCTYPE html>
<html lang="en">
<head>
    %include('header')
    %include('plots/style')
</head>

<body>
%include('navbar')
%include('plots/plot_list')

<div id="flot-3d-json" style="display: none">{{!flot_3d_json}}</div>

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
</body>
</html>
