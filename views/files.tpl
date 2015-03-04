%include('header', title='Menu')

<body onload="init()">
%include('navbar')

<h1>{{cid}}</h1>
<!-- if show cases link here gives an opportunity for another user
     to inspect another persons cases, so disable for now 
{{!cases}}
<hr>
-->

{{!content}}
<hr>

%include('footer')
