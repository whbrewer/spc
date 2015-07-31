%include('header', title='Menu')

<body onload="init()">
%include('navbar')

<h1>{{cid}}</h1>
<!-- if show cases link here gives an opportunity for another user
     to inspect another persons cases, so disable for now 
{{!cases}}
<hr>
-->

%include('navactions')

{{!content}}
<hr>

<div class="bs-example">
    
    <!-- Modal HTML -->
    <div id="myModal" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Content will be loaded here from "remote.php" file -->
            </div>
        </div>

    </div>
</div>

%include('footer')
