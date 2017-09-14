<!DOCTYPE html>
<html lang="en">

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

    <script src="/static/jquery-2.1.4.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/jquery.highlight.js"></script>
    <script src="/static/js/jquery.validate.min.js"></script>
    <script src="/static/js/bootstrap-tagsinput.min.js"></script>
    <script src="/static/js/bootstrap-notify.min.js"></script>
    <script src="/static/js/intro.min.js"></script>
    <script src="/static/js/user_defaults.js"></script>

    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-tagsinput.css">
    <link rel="stylesheet" href="/static/css/introjs.min.css">

    <link rel="alternate stylesheet" href="/static/css/style-classy.css" title="classy">
    <link rel="alternate stylesheet" href="/static/css/style-simple.css" title="simple">
    <link rel="stylesheet" href="/static/css/style-metro.css" title="metro">

    <script> user_defaults() </script>

    <title>
        % if defined('tab_title'):
            {{ tab_title }}
        % else:
            SPC
        % end
    </title>

    <style>

		body {
		    padding-top: 75px;
            padding-bottom: 75px;
		}

    	.modal-lg{ width:850px; }

		.highlight {
		    background-color: #FFFF88;
		}

    </style>

    % if defined('styles'):
        {{ !styles }}
    % end

</head>

<body>
    %include('navbar')
    <div class="container-fluid">
    {{ !base }}
    </div>

    <footer>
        <div class="container-fluid">
            <div id="footModal" class="modal fade">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <!-- Content will be loaded here -->
                    </div>
                </div>
            </div>
        </div>
    </footer>
</body>

</html>
