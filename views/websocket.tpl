<!-- %include('header',title='Monitor') -->
<!-- %include('navbar') -->

<!-- <div id="output"></div> -->

<script>
    var ws = new WebSocket("ws://0.0.0.0:8581/websocket");
    ws.onopen = function() {
        ws.send("Waiting to start...");
    };
    ws.onmessage = function (evt) {
        //alert(evt.data);
        document.getElementById("output").innerHTML += evt.data;
        window.scrollTo(0,document.body.scrollHeight);
    };
</script>

<!-- %include('footer') -->
