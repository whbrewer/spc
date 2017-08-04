% rebase('plots/handson-base.tpl')

<div id="mysheet"></div>

<script>
    var data = {{!data}};

    var container = document.getElementById('mysheet');

    var options = {
        data: data, 
        % if options:
            {{!options}}
        % else:
            rowHeaders: true, 
            colHeaders: true, 
            contextMenu: true 
        % end
    }

    var hot = new Handsontable(container, options);
</script>
