<div id="alert" align="center" class="alert-info">
    %if defined('cid'):
        %if not cid == '':
            <em>NOTE: Using inputs from case id: {{ cid }}</em>
        %else:
            <em>NOTE: Using default inputs</em>
        %end
    %end
</div>
