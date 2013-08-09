<div class="navbar">

<!--<form id="plotform" action="/handler" method="post">-->
<form id="plotform" action="/list" method="post">
<input type="text" class="cid" name="cid" id="cid" value="{{cid}}"/>
<input type="submit" formaction="/plot" class="plot" value="plot"/>
<input type="submit" formaction="/list" class="list" value="list"/>
<input type="submit" formaction="/start" class="start" value="start"/>
<div class="styled-select">
   <select id="app" onchange="this.form.submit()" >
      <option value="mendel">mendel</option>
      <option value="burger">burger</option>
   </select>
</div>
</form>

</div>
