<!DOCTYPE html>
<html lang="en">

<head>

    %include('header')

    % if defined('style'):
    <style>
        {{ !style }}
    </style>
    % end

</head>

<body>
    %include('navbar')

    <div class="container-fluid">
    {{ !base }}
    </div>

    %include('footer')
</body>

</html>
