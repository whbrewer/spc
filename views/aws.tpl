%include('header')
%include('navbar')

<h1>List of EC2 machines</h1>

<table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
    <thead><tr><th>Intance</th><th>Type</th><th>Region</th><th>Actions</th></thead>
    %for i in instances:
        <tr>
            <td>{{i['instance']}}</td> 
            <td>{{i['type']}}</td> 
            <td>{{i['region']}}</td> 
            <td>
                <a href="/aws/status/{{i['id']}}">status</a> 
                <!--<a href="/aws/start/{{i['id']}}">start</a> -->
                <!--<a href="/aws/stop/{{i['id']}}">stop</a> -->
            </td>
        </tr>
    %end
</table> 

%if defined('status'):
    {{status}}
%end

%include('footer')
