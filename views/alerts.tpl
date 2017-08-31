%if defined('alert'):
    % if alert.find("SUCCESS") >= 0:
        <div id="alert" class="alert alert-success alert-dismissable" style="text-align: center">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            {{!alert}}
        </div>
    % elif alert.find("ERROR") >= 0:
        <div id="alert" class="alert alert-danger alert-dismissable" style="text-align: center">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            {{!alert}}
        </div>
    % elif alert.find("WARNING") >= 0:
        <div id="alert" class="alert alert-warning alert-dismissable" style="text-align: center">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            {{!alert}}
        </div>
    % else:
        <div id="alert" class="alert alert-info alert-dismissable" style="text-align: center">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            {{!alert}}
        </div>
    % end
%end
