<html>
<head><style> input { width: 100px; } </style>
</head>
<body>

<h1>Enter parameters:</h1>

<form action="/confirm" method="post">
<table>
<tr><td>case_id:</td><td><input type="text" name="case_id" value="{{case_id}}" size="40" /></td></tr>
<tr><td>mutn_rate:</td><td><input type="text" name="mutn_rate" value="{{mutn_rate}}" size="40" /></td></tr>
<tr><td>frac_fav_mutn:</td><td><input type="text" name="frac_fav_mutn" value="{{frac_fav_mutn}}" size="40" /></td></tr>
<tr><td>reproductive_rate:</td><td><input type="text" name="reproductive_rate" value="{{reproductive_rate}}" size="40" /></td></tr>
<tr><td>pop_size:</td><td><input type="text" name="pop_size" value="{{pop_size}}" size="40" /></td></tr>
<tr><td>num_generations:</td><td><input type="text" name="num_generations" value="{{num_generations}}" size="40" /></td></tr>
</table>
<input type="submit" />

</form>

</body>
</html>
