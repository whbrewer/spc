%rebase('base.tpl')

<ol class="breadcrumb">
  <li><a href="/">Apps</a></li>
  <li><a href="/app/{{app}}">Configure App</a></li>
  <li><a href="/plots/edit?app={{app}}">Plots</a></li>
  <li class="active">Edit</li>
</ol>

<h1>Edit plot definition</h1>

<div id="addplot">
<form class="form-horizontal" method="post" action="/plots/edit/{{row['id']}}">
    <div class="form-group">
        <label for="title" class="control-label col-md-3">Title:</label>
        <div class="col-md-6"><input type="text" class="form-control input-lg" name="title" id="title" value="{{row['title']}}"></div>
    </div>

    <div class="form-group">
        <label for="ptype" class="control-label col-md-3">Type of plot:</label>
        <div class="col-md-6">
          <select name="ptype" id="ptype" class="form-control">
            %opts = {'flot-scatter':'flot/scatter (line, bar, points)', 'flot-scatter-animated':'flot/scatter animated', 'flot-cat':'flot/categories', 'plotly-hist':'plotly/histogram', 'mpl-line':'matplotlib/line', 'mpl-bar':'matplotlib/bar', 'handson':'handsontable'}
            %for key, value in opts.iteritems():
              %if key == row['ptype']:
                <option selected value="{{key}}">{{value}}
              %else:
                <option value="{{key}}">{{value}}
              %end
            %end
          </select>
        </div>
    </div>

    <!-- <div class="form-group">
      <label class="control-label col-md-3">xaxis label:</label>
      <div class="col-md-6">
        <input type="text" class="form-control" name="xaxis_label" id="xaxis_label" onchange="opt()">
      </div>
    </div>

    <div class="form-group">
      <label class="control-label col-md-3">yaxis label:</label>
      <div class="col-md-6">
        <input type="text" class="form-control" name="yaxis_label" id="yaxis_label" onchange="opt()">
      </div>
    </div> -->

    <div class="form-group">
        <label for="options" class="control-label col-md-3">Options (JSON):</label>
        <div class="col-md-6">
            <textarea rows="5" name="options" id="options" class="form-control input-lg">{{row['options']}}</textarea>
        </div>
    </div>

    <input type="hidden" name="app" value="{{app}}">
    <input type="submit" class="btn btn-success center-block" value="Submit">
</form>
</div>
