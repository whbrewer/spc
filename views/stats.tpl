%include('header')
%include('navbar')

<script>

</script>

<h1>Machine Stats</h1>

<div class="container">

<p><b>Jobs</b> running:{{nr}} queued:{{nq}} completed:{{nc}}</p>

<p><b>CPU</b> percent utilization: {{cpu}}%</p>

<p><b>Memory</b> info: {{vm}}%</p>

<p><b>Disk space:</b> {{disk}}</p>

</div>

%include('navactions')

%include('footer')
