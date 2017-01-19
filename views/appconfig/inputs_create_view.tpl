%include("header")

<script>
function add_option_row(x) {
    sel = document.getElementById("html_tags")
    if (x.value == "select") {
        alert("After completing this dialogue, manually edit the template file in views/apps/app.tpl to add options to the select tag.")
        
        // add option to select tag
        // var opt = document.createElement('option')
        // opt.appendChild( document.createTextNode('New Option Text') )
        // opt.value = 'option val'
        // sel.appendChild(opt)
        // var table = document.getElementById("html_tags")

        // add row to table
        //var x = document.getElementById("myTable").rows.length;
        // var row = table.insertRow(0);
        // var cell1 = row.insertCell(0);
        // var cell2 = row.insertCell(1);
        // cell1.innerHTML = "NEW CELL1";
        // cell2.innerHTML = "NEW CELL2";
    }  
}
</script>

<body>

<div class="container-fluid">
<h3>Configure inputs: step 3 of 3</h3>
<br>

<h4>Parsed inputs &ndash; assign html input types</h4>

<form method="post" action="/appconfig/inputs/end">
<input type="submit" class="btn btn-primary" value="Next >>">
<hr>
How to represent a true Boolean value (e.g. T, True, true, 1)?
<input class="form-control" type="text" style="width:100px" name="bool_rep">
<hr>
<table id="html_tags" class="table table-striped">
<thead align=left>
    <th>parameter</th>
    <th>value</th>
    <th>html_tag_type</th>
    <th>description</th>
    <!--<th>data_type</th>-->
</thead>
<tbody>
% import common
% for key,value in inputs.iteritems():
    <tr>
        <td>{{key}}</td> <td>{{value}}</td> 
        <td><select class="form-control" id="html_tags" name="html_tags"  
                    onchange="add_option_row(this)">
            % vtype = common.type(value)
            % if vtype == "number":
                <option selected value="number">number
                <option value="text">text
                <option value="checkbox">checkbox            
            % elif vtype == "bool":
                <option selected value="checkbox">checkbox
                <option value="number">number
                <option value="text">text
            % else:
                <option selected value="text">text
                <option value="number">number
                <option value="checkbox">checkbox            
            % end
            <option value="hidden">hidden
            <option value="select">select
            <option value="textarea">textarea
        </select></td>
        <!--
        <td><select name="data_type">
            <option value="string">String
            <option value="integer">Integer
            <option value="float">Float
            <option value="boolean">Boolean
        </select></td>
        -->
        <td><input class="form-control" type="text" name="descriptions" value="{{key}}"></td>
    </tr>
    <input type="hidden" name="keys" value="{{key}}">
    <input type="hidden" name="appname" value="{{appname}}">
    <input type="hidden" name="input_format" value="{{input_format}}">
% end
</tbody>
</table>
</form>

<hr>
</div>

%include('footer')

