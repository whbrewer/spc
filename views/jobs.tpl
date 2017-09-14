<%
    style = """
      .glyphicon.glyphicon-star, .glyphicon.glyphicon-star-empty {
        font-size: 120%;
      }
      .table {
        font-size: 120%;
      }
    """
    rebase('base.tpl', style=style)
%>

<div class="container-fluid">
    <div class="row">

          <div class="col-xs-12 col-sm-3">
            <form action="/jobs">
              <input name="q" type="text" class="form-control input-lg"
                   onchange="show(this.value)" style="background-color:#faffbd" placeholder="Search..." value="{{q}}">
            </form>
          </div>

          <div class="btn-group col-xs-6" id="actions" style="display:none">
              <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#dModal"><span class="glyphicon glyphicon-trash"></span> Delete</button>

              <button type="button" class="btn btn-warning" data-toggle="modal"  data-target="#mergeModal"><span class="glyphicon glyphicon-resize-small"></span> Merge</button>
          </div>

          <div class="btn-group col-xs-3">
              <form id="diff_button" class="btn-group" style="display:none" action="/jobs/diff">
                  <button type="submit" class="btn btn-primary"><span class="glyphicon glyphicon-scale"></span> Diff</button>
              </form>
          </div>

    </div>
</div>

<!--<meta http-equiv="refresh" content="5">-->
<table id="clickable" class="table table-striped">
<thead>
<tr>
  <th><input type="checkbox" onchange="toggle(this); toggle_action_button_visibility()"></th>
  <th><a href="/jobs?starred=1"><span class="glyphicon glyphicon-star"></span></a></th>
  <th>cid</th>
  <th>app</th>
  <th>state</th>
  %if np > 1:
    <th class="hidden-xs hidden-sm hidden-md">np</th>
  %end
  <!-- <th class="hidden-xs hidden-sm hidden-md">priority</th> -->
  <th class="hidden-xs">date/time submitted</th>
  <th class="hidden-xs hidden-sm hidden-md">walltime (s)</th>
  <th class="hidden-xs">labels</th>
  <th><a href="/jobs?shared=1" title="see shared cases"><span class="glyphicon glyphicon-pushpin"></span></a></th>
</tr>
</thead>

<tbody>
%for row in rows:
  <tr>
    <td><input type="checkbox" name="selected_cases" value="{{row['id']}}:" onchange="toggle_action_button_visibility()"></td>
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
    <td class="case"><samp>{{row['cid']}}</samp> <a href="{{url}}"></a></td>
    <td class="case"><samp>{{row['app']}} <a href="{{url}}"></a></samp></td>
    <td class="case"><samp><a id="job-{{row['id']}}" onclick="get_remote_job_status({{row['id']}})">{{row['state']}}</a></samp> <a href="{{url}}"></a></td>
    %if np > 1:
      <td class="case hidden-xs hidden-sm hidden-md">{{row['np']}} <a href="{{url}}"></a></td>
    %end
    <!-- <td class="case hidden-xs hidden-sm hidden-md"><samp>{{row['priority']}}</samp> <a href="{{url}}"></a></td> -->
    <td class="case hidden-xs"><samp>{{row['time_submit']}}</samp> <a href="{{url}}"></a></td>
    <td class="case hidden-xs hidden-sm hidden-md"><samp>{{row['walltime']}}</samp> <a href="{{url}}"></a></td>
    <td class="case hidden-xs"><samp>{{!row['description']}}</samp>
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

<form method="get" action="/jobs">
  <input type="hidden" name="n" value="{{n+num_rows}}">
  <input type="submit" class="btn btn-default btn-block" value="Show more">
</form>

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
                    <button type="submit" class="btn btn-danger center-block">Delete</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Merge Modal -->
<div class="modal fade" id="mergeModal" tabindex="-1" role="dialog"
     aria-labelledby="mergeModal">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <form id="merge_modal" class="form-horizontal" method="post" action="/jobs/merge">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title">What do you want do with the selected cases?</h4>
                </div>
                <div class="modal-footer">
                    <div class="form-group">
                        <label class="control-label col-xs-12 col-sm-6">Files to merge:</label>
                        <div class="col-xs-12 col-sm-6">
                            <input type="text" name="file_pattern" class="form-control input-lg" value="<cid>.000.plm" />
                        </div>
                    </div>

                    <div class="btn-group">
                        <button type="submit" formaction="/jobs/merge/sum" class="btn btn-default"><span class="glyphicon glyphicon-plus"></span> Sum</button>
                        <button type="submit" formaction="/jobs/merge/avg" class="btn btn-default"> Average</button>
                    </div>
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
    checkboxes[i].checked = source.checked
  }
}

function toggle_action_button_visibility() {
  var checkboxes = document.getElementsByName('selected_cases')
  var show = false
  var values = ""
  var count = 0
  for(var i=0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      show = true;
      values += checkboxes[i].value
      count += 1
    }
  }

  var dom = document.getElementById("actions")
  if (show) {
    dom.style.display = "block"
  } else {
    dom.style.display = "none"
  }

  var dom2 = document.getElementById("diff_button")
  if (count == 2) {
      dom2.style.display = "block"
  } else {
      dom2.style.display = "none"
  }

  // cases to be deleted
  var input = document.getElementById("selected_cases")

  if(input) { // if user has already checked some cases modify the cases to be deleted
      input.value = values
  } else { // otherwise create a new hidden input element on delete form
      var deleteForm = document.getElementById("delete_modal")
      input = document.createElement('input')
      input.type = 'hidden'
      input.name = 'selected_cases'
      input.id = 'selected_cases'
      input.value = values
      deleteForm.appendChild(input)
  }

  // cases to be merged
  var input = document.getElementById("selected_merge_cases")

  if(input) { // if user has already checked some cases modify the cases to be deleted
      input.value = values
  } else { // otherwise create a new hidden input element on delete form
      var mergeForm = document.getElementById("merge_modal")
      input = document.createElement('input')
      input.type = 'hidden'
      input.name = 'selected_merge_cases'
      input.id = 'selected_merge_cases'
      input.value = values
      mergeForm.appendChild(input)
  }

  // cases to be diffed
  var input = document.getElementById("selected_diff_cases")

  if(input) { // if user has already checked some cases modify the cases to be deleted
      input.value = values
  } else { // otherwise create a new hidden input element on diff form
      var diffForm = document.getElementById("diff_button")
      input = document.createElement('input')
      input.type = 'hidden'
      input.name = 'selected_diff_cases'
      input.id = 'selected_diff_cases'
      input.value = values
      diffForm.appendChild(input)
  }

}
</script>
