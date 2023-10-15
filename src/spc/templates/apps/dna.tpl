%rebase('base.tpl')
%include('apps/alert')

<form action="/confirm" method="post">
<input type="hidden" name="app" value="{{app}}">
<input type="hidden" name="cid" value="{{cid}}">

<button type="submit" class="btn btn-success"> <!-- pull-right -->
Continue <em class="glyphicon glyphicon-forward"></em>
</button>

<div class="container-fluid">
<h2>Enter string of DNA to be analyzed:</h2>
<textarea class="form-control" name="dna" rows="4" cols="80">
{{dna}}
</textarea>
</div>

</form>
