%rebase('base.tpl')

<h1>{{user}}'s account</h1>
<br>

%if user == "guest":
<p>Guest account password can only be changed by the administrator.</p>
%else:
<fieldset>

    <legend>Change Password</legend>
    <form class="form-horizontal" method="POST" action="/account/change_password">

        <div class="form-group">
            <label class="control-label col-xs-6">Old password:</label>
            <div class="formcontrol col-xs-6">
                <input class="form-control" type="password" name="opasswd">
            </div>
        </div>

        <div class="form-group">
            <label class="control-label col-xs-6">New password:</label>
            <div class="formcontrol col-xs-6">
                <input class="form-control" type="password" name="npasswd1">
            </div>
        </div>

        <div class="form-group">
            <label class="control-label col-xs-6">New password (again):</label>
            <div class="formcontrol col-xs-6">
                <input class="form-control" type="password" name="npasswd2">
            </div>
        </div>

        <input class="btn btn-default" type="submit">

    </form>

</fieldset>
%end

<fieldset>
<legend>Upload data to account</legend>
<form action="/upload" method="post" enctype="multipart/form-data">
  <!-- Category: <input type="text" name="category" /> -->
  <h4>Select a file:</h4>
  <input type="file" name="upload" /><br>
  <input class="btn btn-default" type="submit" value="Upload"/>
</form>
</fieldset>

<fieldset>
<legend>Set Theme</legend>
    <form class="btn-group">
        <button type="radio" class="btn btn-default" onclick="switch_style('simple');return false;" name="theme" id="simple">Simpleton</button>
        <button type="radio" class="btn btn-default" onclick="switch_style('metro');return false;" name="theme" id="metro">Metro</button>
        <button type="radio" class="btn btn-default" onclick="switch_style('classy');return false;" name="theme" id="classy">Classy</button>
    </form>
</fieldset>
