%include('header')
%include('navbar')

<script>
function verifyInstance(itype) {
    re = /i-\d{8}/
    if (itype.search(re) < 0) {
        alert("Wrong instance type. Format should be like: i-01234567")
    }
}
</script>

<h1>Amazon Web Services (AWS)</h1>

<br>
<fieldset>
<legend>AWS credentials</legend>
<table class="table table-striped">
<thead>
<tr>
   <th>account_id</th>
   <th>secret</th>
   <th>key</th>
   <th>action</th>
</tr>
</thead>
%if creds:
    %for c in creds:
    <tr>
    <td>{{c['account_id']}}</td>
    <td>{{c['secret']}}</td>
    <td>{{c['key']}}</td>
    <td><form method="POST" action="/aws/cred/delete">
        <input type="hidden" name="id" value="{{c['id']}}">
        <input type="submit" value="Delete"</a>
        </form></td>
    </tr>
    %end
%else:
    <form method="POST" action="/aws/creds">
    <tr> <td><input type="text" name="account_id" size=12></td> 
         <td><input type="text" name="secret" size=40></td> 
         <td><input type="text" name="key" size=20></td> 
         <td><input type="submit" class="btn btn-default" value="Add"></td></tr>
    </form>
%end
</table>
</fieldset>

<br>

<fieldset>
<legend>EC2 instances</legend>

<table class="table table-striped">
    <thead><tr><th>Intance id</th><th>Type</th><th>Region</th><th>Actions</th></thead>
    %for i in instances:
        <tr>
            <td>{{i['instance']}}</td> 
            <td>{{i['itype']}}</td> 
            <td>{{i['region']}}</td> 
            <td>
                <a href="/aws/status/{{i['id']}}">status</a> 
                <!--<a href="/aws/start/{{i['id']}}">start</a> -->
                <!--<a href="/aws/stop/{{i['id']}}">stop</a> -->
            </td>
        </tr>
    %end

<form method="POST" action="/aws/instance">
<td><input type="text" size=10 name="instance" onchange="verifyInstance(this.value)"></td>
<td>
<select name="itype">
<option disabled role=separator>General purpose:
<option value="t1.micro">t1.micro
<option value="t2.micro">t2.micro
<option value="t2.small">t2.small
<option value="t2.medium">t2.medium
<option disabled role=separator>-
<option value="m3.medium">m3.medium
<option value="m3.large">m3.large
<option value="m3.xlarge">m3.xlarge
<option value="m3.2xlarge">m3.2xlarge
<option disabled role=separator>Compute optimized:
<option value="c3.large">c3.large
<option value="c3.xlarge">c3.xlarge
<option value="c3.2xlarge">c3.2xlarge
<option value="c3.3xlarge">c3.3xlarge
<option value="c3.8xlarge">c3.8xlarge
<option disabled role=separator>-
<option value="c4.large">c4.large
<option value="c4.xlarge">c4.xlarge
<option value="c4.2xlarge">c4.2xlarge
<option value="c4.4xlarge">c4.4xlarge
<option value="c4.8xlarge">c4.8xlarge
<option disabled role=separator>Memory optimized:
<option value="r3.large">r3.large
<option value="r3.xlarge">r3.xlarge
<option value="r3.2xlarge">r3.2xlarge
<option value="r3.3xlarge">r3.3xlarge
<option value="r3.8xlarge">r3.8xlarge
<option disabled role=separator>GPU:
<option value="r3.large">g2.2xlarge
<option disabled role=separator>Storage optimized:
<option value="i2.large">i2.large
<option value="i2.xlarge">i2.xlarge
<option value="i2.2xlarge">i2.2xlarge
<option value="i2.3xlarge">i2.3xlarge
<option value="i2.8xlarge">i2.8xlarge
</option>
</select>
</td>

<td>
<select name="region">
<option value="ap-northeast-1">  Asia Pacific (Tokyo)
<option value="ap-southeast-2">  Asia Pacific (Sydney)
<option value="ap-southeast-1">  Asia Pacific (Singapore)
<option value="eu-west-1">       EU (Ireland)
<option value="eu-central-1">    EU (Frankfurt) 
<option value="sa-east-1">       South America (Sao Paulo)
<option value="us-east-1">       US East (N. Virginia)
<option value="us-west-1">       US West (N. California)
<option value="us-west-2">       US West (Oregon)
</option>
</select>
</td>

<td> <input type="submit" class="btn btn-default" value="Add"> </td>
</table>
</form>
</fieldset>


%include('footer')
