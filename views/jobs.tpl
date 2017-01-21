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

    function get_remote_job_status(jid) {
      $.get( "http://localhost:8581/status/"+jid, function (data) {
        $("#job-"+jid).html(data);
      });
    };

    function toggle(source) {
      checkboxes = document.getElementsByName('selected_cases');
      for(var i=0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
      }
    }

    function toggle_delete_button_visibility() {
      var checkboxes = document.getElementsByName('selected_cases');
      var show = false;
      var values = "";
      for(var i=0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
          show = true;
          values += checkboxes[i].value;
        }
      }

      var dom = document.getElementById("delete_button")
      if (show) {
        dom.style.display = "block";
      } else {
        dom.style.display = "none";
      }

      var input = document.getElementById("selected_cases")
      if(input) { // if user has already checked some cases just modify the cases to be deleted
        input.value = values;
      } else { // otherwise create a new hidden input element
        var theForm = document.getElementById("delete_modal");
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_cases';
        input.id = 'selected_cases';
        input.value = values;
        theForm.appendChild(input);
      }

    }

</script>

<body>
%include('navbar')

<div class="col-xs-12" style="height:10px"></div>

<div class="row">
  <div class="col-xs-6">
    <form role="form" action="/jobs">
      <input name="q" type="text" class="form-control input-lg"
           onchange="show(this.value)" style="background-color:#faffbd" placeholder="Search..." value="{{q}}">
    </form>
  </div>

  <form>
  <div class="col-xs-6">
  <button id="delete_button" type="button" class="btn btn-danger" data-toggle="modal" data-target="#dModal" style="display:none"><span class="glyphicon glyphicon-trash"></span> Delete</button>
  </div>

</div>

<!--<meta http-equiv="refresh" content="5">-->
<table id="clickable" class="table table-striped">
<thead>
<tr>
  <th><input type="checkbox" onchange="toggle(this); toggle_delete_button_visibility()"></th>
  <th><a href="/jobs?starred=1"><span class="glyphicon glyphicon-star"></span></a></th>
  <th>cid</th> 
  <th>app</th> 
  <th>state</th>
  %if np > 1: 
    <th class="hidden-xs hidden-sm hidden-md">np</th>
  %end 
  %if sched == "mp":
    <th class="hidden-xs hidden-sm hidden-md">priority</th> 
  %end
  <th class="hidden-xs">date/time submitted</th> 
  <th class="hidden-xs hidden-sm hidden-md">walltime (s)</th>
  <th class="hidden-xs">labels</th>
  <th><a href="/jobs?shared=1" title="see shared cases"><span class="glyphicon glyphicon-pushpin"></span></a></th>
</tr>
</thead>

<tbody>
%for row in rows:
  <tr>
    <td><input type="checkbox" name="selected_cases" value="{{row['id']}}:" onchange="toggle_delete_button_visibility()"></td>
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
    %url="/case?cid="+row['cid']+"&app="+row['app']+"&jid="+str(row['id'])
    <td class="case"><tt>{{row['cid']}}</tt></td>
    <td class="case">{{row['app']}} <a href="{{url}}"></a></td>
    <td class="case"><tt><a id="job-{{row['state']}}" onclick="get_remote_job_status({{row['state']}})">{{row['state']}}</a></tt> <a href="{{url}}"></a></td>
    %if np > 1:
      <td class="case hidden-xs hidden-sm hidden-md">{{row['np']}} <a href="{{url}}"></a></td>
    %end
    %if sched == "mp":
      <td class="case hidden-xs hidden-sm hidden-md"><tt>{{row['priority']}}</tt> <a href="{{url}}"></a></td>
    %end
    <td class="case hidden-xs"><tt>{{row['time_submit']}}</tt> <a href="{{url}}"></a></td>
    <td class="case hidden-xs hidden-sm hidden-md"><tt>{{row['walltime']}}</tt> <a href="{{url}}"></a></td>
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
</tr> 
%end
</tbody>
</table>
</form>

<form method="get" action="/jobs">
  <input type="hidden" name="n" value="{{n+num_rows}}">
  <input type="submit" class="btn btn-default btn-block" value="Show more">
</form>

<footer class="footer">
  <div class="container">
    <p class="text-muted" align=center>running:{{nr}} queued:{{nq}} completed:{{nc}}</p>
  </div>
</footer>

<!-- Delete Modal -->
<div class="modal fade" id="dModal" tabindex="-1" role="dialog" 
     aria-labelledby="deleteModal">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <form id="delete_modal" class="form-horizontal" method="post" action="/jobs/delete_selected_cases">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" id="deleteModal">Delete Selected Cases?</h4>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-danger">Delete</button>
                </div>
            </form>
        </div>
    </div>
</div>

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
