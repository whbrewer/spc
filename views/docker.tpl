%include('header')
%include('navbar')

<!-- <h1>Docker Containers</h1>

<br>
<fieldset>
<legend>Docker Settings</legend>
    <form method="POST" action="/docker/config">
    <label for="host">Docker Host:</label><input class="form-control" type="text" name="host" size=40 value="{{host}}" placeholder="localhost"><br />
    <label for="image">Docker Image:</label><input class="form-control" type="text" name="image" size=40 value="{{image}}" placeholder="ubuntu:14.04"><br />
    <input class="btn btn-default" type="submit" value="Update">
    </form>
</fieldset> -->

<br>

<fieldset>
<legend>Docker containers</legend>

<table class="table table-striped">
    <thead><tr><th>Container id</th><th>Image</th><th>Command</th><th>Actions</th></thead>
    %for i in instances:
        <tr>
            <td>{{i['containerid']}}</td>
            <td>{{i['image']}}</td>
            <td>{{i['command']}}</td>
            <td>
                <a href="/docker/status/{{i['id']}}">status</a> ::
                <a href="/docker/start/{{i['id']}}">start</a> ::
                <a href="/docker/stop/{{i['id']}}">stop</a> 
            </td>
        </tr>
    %end

<tr>
<form method="POST" action="/docker/container">
    <td><input class="form-control" type="text" size=10 name="containerid"></td>
    <td><input class="form-control" type="text" size=10 name="image"></td>
    <td><input class="form-control" type="text" size=10 name="command"></td>
    <td> <input class="btn btn-default" type="submit" value="Add"> </td>
</form>
</tr>
</table>
</fieldset>


%include('footer')
