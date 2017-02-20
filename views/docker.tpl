%include('header')
%include('navbar')
% import datetime, re, urllib

<body>

<h2>Docker Containers</h2>

<table class="table table-striped">
<thead><tr><th>CONTAINER ID</th><th>IMAGE</th><th>COMMAND</th><th>CREATED</th><th>STATUS</th><th>NAMES</th><th>ACTIONS</th></tr></thead>
% for c in containers:
    <tr>
        <!-- <td>{{c}}</td> -->
        <td>{{c['Id'][:12]}}</td>
        <td>{{c['Image']}}</td>
        <td>{{c['Command']}}</td>
        <td>{{datetime.datetime.fromtimestamp(c['Created'])}}</td>
        <td>{{c['Status']}}</td>
        <!-- <td>{{c['Ports']}}</td> -->
        <td>
        % for n in c['Names']:
            {{n[1:]}}
        % end
        </td>
        <td>
        % if re.search("Exited", c['Status']) or re.search("Created", c['Status']):
            <a href="/docker/start/{{c['Id'][:12]}}"><span class="glyphicon glyphicon-play"></span></a> <a href="/docker/remove/{{c['Id'][:12]}}"><span class="glyphicon glyphicon-remove-circle"></span></a>
        % else:
            <a href="/docker/stop/{{c['Id'][:12]}}"><span class="glyphicon glyphicon-stop"></span></a>
        % end
    </tr>
%end
</table>

<hr>

<h2>Docker Images</h2>

<!--  % def sha(x): x.split(":")[1] -->
<table class="table table-striped">
    <thead><tr><th>REPOSITORY</th><th>IMAGE ID</th><th>CREATED</th><th>SIZE</th><th>ACTIONS</th></tr></thead>
    % for i in images:
        % for t in i['RepoTags']:
            <tr>
                <td>{{t}}</td>
                % _, id = i['Id'].split(":")
                <td>{{id[:12]}}</td>
                <td>{{datetime.datetime.fromtimestamp(i['Created'])}}</td>
                % from common import sizeof_fmt
                <td>{{sizeof_fmt(i['Size'])}}</td>
                <td><a href="/docker/create/{{id[:12]}}"><span class="glyphicon glyphicon-new-window"></span></a> &nbsp;&nbsp;
                    <a href="/docker/remove_image/{{t}}"><span class="glyphicon glyphicon-remove-circle"></span></a>
                </td>
            </tr>
        % end
    % end

</table>

%include('footer')
