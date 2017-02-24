<html>
<head>

    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

    <script src="/static/jquery-2.1.4.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/jquery.highlight.js"></script>
    <script src="/static/js/jquery.validate.min.js"></script>
    <script src="/static/js/bootstrap-tagsinput.min.js"></script>
    <script src="/static/js/intro.min.js"></script>
    <script src="/static/js/user_defaults.js"></script>

    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-tagsinput.css">
    <link rel="stylesheet" href="/static/css/introjs.min.css">

    <link rel="alternate stylesheet" href="/static/css/style-class.css" title="classy">
    <link rel="alternate stylesheet" href="/static/css/style-simple.css" title="simple">
    <link rel="stylesheet" href="/static/css/style-metro.css" title="metro">

    <script> user_defaults() </script>

    <style>

		body {
		    padding-top: 75px;
		    /* If fixing the navactions bar use 100px */
		    /*padding-top: 100px;*/
            padding-bottom: 75px;
		}

    	.modal-lg{ width:850px; }

		.highlight {
		    background-color: #FFFF88;
		}

    </style>

    <script>
       document.body.onload = function() {
           document.title = location.host;
       }
    </script>

</head>

<!-- can comment out if using ajax or just ignore which will give unnoticeable JS error -->
<!-- %include('websocket') -->

<div class="container-fluid">
