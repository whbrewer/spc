%include header title='Edit App'

<body onload="init()">
<script>
function delete(id) {
   if(!confirm("Are you sure to delete?")) return                      
      document.student_modify.action = "/apps/delete/id"
      document.student_modify.submit()
   }
}
</script>

<form method="post" action="/apps/edit">
App name:    <input type="text" name="appname" value="{{appname}}"><br>
Description: <textarea name="description" value="{{appname}}"></textarea><br>
Category: 
<select name="category" onchange="somefn()">
   <option SELECTED value="bioinformatics">Bioinformatics
   <option value="cfd">CFD
   <option value="other">Other
</select>

<br>Language:
<select name="language">
   <option SELECTED value="python">Python
   <option value="fortran">Fortran
   <option value="c">C
</select>

</form>

%include footer
