%rebase('base.tpl')

<h1>Machine Stats</h1>

<div class="container">

<!-- <p><b>Jobs</b> running:{{nr}} queued:{{nq}} completed:{{nc}}</p> -->

<table class="table table-striped">
<tr> <td width="200">CPU</td> <td>{{cpu}}%</td> </tr>
<tr> <td>Memory</td> <td>{{vm}}%</td> </tr>
<tr> <td>Disk usage</td> <td>{{disk}}%</td> </tr>
<tr> <td>Jobs Running</td> <td>{{nr}}</td> </tr>
<tr> <td>Jobs Queued</td> <td>{{nq}}</td> </tr>
<tr> <td>Jobs Completed</td> <td>{{nc}}</td> </tr>
</table>

<!-- <p><b>CPU</b> utilization: {{cpu}}%</p>

<p><b>Memory</b> utilization: {{vm}}%</p>

<p><b>Disk usage:</b> {{disk}}%</p> -->

</div>

%include('navactions')
