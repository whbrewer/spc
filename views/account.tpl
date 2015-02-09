%include('header')
%include('navbar')

<h1>My Account</h1>
<br>

<fieldset>
<legend>Change Password</legend>
<form method="POST" action="/account/change_password">
<table>
<tr><td>Old password:</td> <td><input type="password" name="opasswd"></td></tr>
<tr><td>New password:</td> <td><input type="password" name="npasswd1"></td></tr>
<tr><td>New password (again):</td> <td><input type="password" name="npasswd2"></td></tr>
</table>
<input type="submit">
</form>
</fieldset>

%include('footer')
