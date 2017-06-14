<div id="alert" class="alert-info hidden-xs" style="text-align: center">
    %if defined('cid'):
        %if not cid == '':
            <em>NOTE: Using inputs from case id: {{ cid }}</em>
        %else:
            <em>NOTE: Using default inputs</em>
        %end
    %end
</div>
