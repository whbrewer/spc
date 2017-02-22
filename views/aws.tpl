%include('header')
%include('navbar')

<script>

function verifyInstance(itype) {
    re = /^i-(\w{8}|\w{17})$/
    if (itype.search(re) < 0) {
        $("#feedback").html("Format should be like: i-012345678 or longer type i-1234567890abcdefg")
    } else {
        $("#feedback").html("")
    }
}

function delInstance(aid) {
    var result = confirm("Are you sure you want to delete this instance?");
    if (result) {
        $.ajax({ url: "/aws/instance/" + aid, type: "DELETE" })
        location.reload(true)
    }
}

function delCreds(id) {
    var result = confirm("Are you sure you want to delete these credentials?");
    if (result) {
        $.ajax({ url: "/aws/creds/" + id, type: "DELETE" })
        location.reload(true)
    }
}

function toggleAddInstance() {
    $(".editable").show()
}
</script>

<body>

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
</tr>
</thead>
%if creds:
    %for c in creds:
        <tr>
            <td><a onclick="delCreds({{c['id']}})"><span class="glyphicon glyphicon-remove editable" style="display:none"></span></a></td>
            <td>{{c['account_id']}}</td>
            <td>{{c['secret']}}</td>
            <td>{{c['key']}}</td>
        </tr>
    %end
%else:
    <form method="POST" action="/aws/creds">
    <tr> <td><input class="form-control" type="text" name="account_id" size=12></td>
         <td><input class="form-control" type="text" name="secret" size=40></td>
         <td><input class="form-control" type="text" name="key" size=20></td>
         <td><input class="form-control" type="submit" class="btn btn-primary" value="Add"></td></tr>
    </form>
%end
</table>
</fieldset>

<br>

<fieldset>
<legend>EC2 instances</legend>

<span id="feedback" class="text-danger"></span>

<table class="table table-striped">
    <thead><tr><th></th><th>Intance id</th><th>Type</th><th>Region</th><th>Rate</th><th>Actions</th></thead>
    <tbody>
    %for i in instances:
        <tr>
            <td><button class="btn btn-link editable" style="display:none" onclick="delInstance({{i['id']}})"><span class="glyphicon glyphicon-remove"></span></button></td>
            <td>{{i['instance']}}</td>
            <td>{{i['itype']}}</td>
            <td>{{i['region']}}</td>
            <td>{{i['rate']}}</td>
            <td>
                <!-- <select class="form-control" name="action">
                    <option "status"><span class="glyphicon glyphicon-info-sign"></span> status</option>
                    <option "start"><span class="glyphicon glyphicon-play"></span> start</option>
                    <option "stop"><span class="glyphicon glyphicon-stop"></span> stop</option>
                    <option "delete"><span class="glyphicon glyphicon-delete"></span> delete</option>
                </select> -->
                <a class="btn btn-default" href="/aws/status/{{i['id']}}"><span class="glyphicon glyphicon-info-sign"></span> status</a>

                <!--<a href="/aws/start/{{i['id']}}">start</a> -->
                <!--<a href="/aws/stop/{{i['id']}}">stop</a> -->
            </td>
        </tr>
    %end

    <tr class="editable" style="display:none">

    <form method="POST" action="/aws/instance">
    <td></td>
    <td><input class="form-control" type="text" size=10 name="instance" onkeyup="verifyInstance(this.value)"></td>
    <td>
    <select class="form-control btn-lg" name="itype">
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
    <option value="m4.4xlarge">m4.4xlarge
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
    <select class="form-control btn-lg" name="region">
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

    <td> <input type="number" min="0" step="any" class="form-control" style="width:100px" name="rate"> </td>

    <td> <input type="submit" class="btn btn-link" value="add instance"> </td>
    </form>

    </tr>

    </tbody>
</table>

</fieldset>

<a class="btn" onclick="toggleAddInstance()"><span class="glyphicon glyphicon-wrench"></span> Configure</a>

<!-- Delete Modal -->
<div class="modal fade" id="dModal" tabindex="-1" role="dialog"
     aria-labelledby="deleteModal">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <form id="delete_modal" class="form-horizontal" method="post" action="/jobs/delete_selected
_cases">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" id="deleteModal">Delete Selected Cases?</h4>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Delete</button>
                </div>
            </form>
        </div>
    </div>
</div>


%include('footer')
