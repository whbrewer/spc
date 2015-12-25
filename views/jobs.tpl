%include('header')

<style>
  .glyphicon.glyphicon-star, .glyphicon.glyphicon-star-empty {
    font-size: 120%;
  }
  .table {
    font-size: 120%;
  }
</style>

<script>
    function star(jid) {
      $('#'+jid).toggleClass('glyphicon-star-empty');
      $('#'+jid).toggleClass('glyphicon-star');
      $.post('/jobs/star', { 'jid': jid });
    };

    function unstar(jid) {
      $('#'+jid).toggleClass('glyphicon-star-empty');
      $('#'+jid).toggleClass('glyphicon-star');
      $.post('/jobs/unstar', { 'jid': jid });
    };

    function share(jid) {
      $('#shared'+jid).toggleClass('glyphicon-share-alt');
      $('#shared'+jid).toggleClass('glyphicon-pushpin');
      $.post('/jobs/share', { 'jid': jid });
    };

    function unshare(jid) {
      $('#shared'+jid).toggleClass('glyphicon-share-alt');
      $('#shared'+jid).toggleClass('glyphicon-pushpin');
      $.post('/jobs/unshare', { 'jid': jid });
    };
</script>

<body>
%include('navbar')

<div class="col-xs-12" style="height:10px"></div>

<div class="col-xs-12">
  <form role="form" action="/jobs">
    <input name="q" type="text" class="form-control input-lg"
         onchange="show(this.value)" placeholder="Search labels...">
  </form>
</div>

<!--<meta http-equiv="refresh" content="5">-->
<table id="clickable" class="table table-striped">
<thead>
<tr>
  <th><a href="/jobs?starred=1"><span class="glyphicon glyphicon-star"></span></a></th>
  <th class="hidden-xs">jid</th> 
  <th>app</th> 
  <th>cid</th> 
  <th>state</th>
  %if np > 1: 
    <th class="hidden-xs">np</th>
  %end 
  %if sched == "smp":
    <th>priority</th> 
  %end
  <th class="hidden-xs">date/time submitted</th> 
  <th class="hidden-xs">labels</th>
  <th><a href="/jobs?shared=1" title="see shared cases"><span class="glyphicon glyphicon-pushpin"></span></a></th>
</tr>
</thead>

<tbody>
%for row in rows:
  <tr>
  <form>
  %if row['starred']=="True":
    <td>
      <a href="javascript:unstar({{row['id']}})">
        <span id="{{row['id']}}" class="glyphicon glyphicon-star"></span></a>
    </td>
  %else:
    <td>
      <a href="javascript:star({{row['id']}})">
        <span id="{{row['id']}}"  class="glyphicon glyphicon-star-empty"></span></a>
    </td>
  %end
  <div>
    %url="/case?cid="+row['cid']+"&app="+row['app']+"&jid="+str(row['id'])
    <td class="case hidden-xs">{{row['id']}} <a href="{{url}}"></a></td>
    <td class="case">{{row['app']}} <a href="{{url}}"></a></td>
    <td class="case"><tt>{{row['cid']}}</tt> <a href="{{url}}"></a></td>
    <td class="case"><tt>{{row['state']}}</tt> <a href="{{url}}"></a></td>
    %if np > 1:
      <td class="case hidden-xs">{{row['np']}} <a href="{{url}}"></a></td>
    %end
    %if sched == "smp":
      <td class="case hidden-xs"><tt>{{row['priority']}}</tt> <a href="{{url}}"></a></td>
    %end
    <td class="case hidden-xs"><tt>{{row['time_submit']}}</tt> <a href="{{url}}"></a></td>
    <td class="case hidden-xs"> {{row['description']}}
      <!-- <a href="/case?cid={{row['cid']}}&app={{row['app']}}&jid={{row['id']}}"></a> -->
      <a href="{{url}}"> </a>
    </td>
  %if row['shared']=="True":
    <td>
      <a href="javascript:unshare({{row['id']}})" title="unshare this case">
        <span id="shared{{row['id']}}" class="glyphicon glyphicon-pushpin"></span></a>
    </td>
  %else:
    <td>
      <a href="javascript:share({{row['id']}})" title="share this case with other users">
        <span id="shared{{row['id']}}"  class="glyphicon glyphicon-share-alt"></span></a>
    </td>
  %end
  </div>
  </form>
</tr> 
%end
</tbody>
</table>

<form method="get" action="/jobs">
  <input type="hidden" name="n" value="{{n+num_rows}}">
  <input type="submit" class="btn btn-default btn-block" value="Show more">
</form>

<script>
$(document).ready(function() {
    // $('#clickable tr').click(function(e) {
    $('.case').click(function(e) {
        var href = $(this).find("a").attr("href");
        if(href) { window.location = href; }
        e.stopPropagation();
    });
});
</script>
%include('footer')
