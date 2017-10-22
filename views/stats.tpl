%rebase('base.tpl')

<h1>Machine Stats</h1>

<div class="container">

<p><b>Jobs</b> running:{{nr}} queued:{{nq}} completed:{{nc}}</p>

<p><b>CPU</b> utilization: {{cpu}}%</p>

<p><b>Memory</b> utilization: {{vm}}%</p>

<p><b>Disk usage:</b> {{disk}}%</p>

</div>

%include('navactions')
