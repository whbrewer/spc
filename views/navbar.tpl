<div class="navbar">

<form id="plotform" action="/list" method="post">
<input type="text" class="cid" name="cid" id="cid" value="{{cid}}"/>
<input type="submit" formaction="/start" class="start" value="start"/>
<input type="submit" formaction="/plot" class="plot" value="plot"/>
<input type="submit" formaction="/list" class="list" value="list"/>
<input type="submit" formaction="/output" class="output" value="output"/>
<div class="styled-select">
   <select name="app" id="app" onchange="this.form.submit()" >
      <option value="mendel">mendel</option>
      <option value="burger">burger</option>
   </select>
</div>
</form>

</div>
