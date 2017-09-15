<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
    %include('header')
    <script src="/static/js/flot/excanvas.min.js"></script>
    <script src="/static/js/flot/jquery.min.js"></script>
    <script src="/static/js/flot/jquery.flot.js"></script>
    <script src="/static/js/flot/jquery.flot.axislabels.min.js"></script>
    <script src="/static/js/flot/jquery.flot.selection.min.js"></script>
    <script src="/static/js/flot/jquery.flot.fillbetween.min.js"></script>
    <script src="/static/js/flot/jquery.flot.resize.min.js"></script>
    <script src="/static/js/flot/jquery.flot.stack.min.js"></script>
    <script src="/static/js/flot/jquery.flot.animator.min.js"></script>
    <!-- <script src="/static/js/flot/jquery.flot.navigate.min.js"></script> -->
    <!-- <script src="/static/js/canvas2image.js"></script> -->
    %include('plots/style')
</head>

<body>
%include('navbar')
%include('plots/plot_list')

{{!base}}

%include('footer')
</body>
</html>
