%if defined('status'):
    % if status.find("SUCCESS") >= 0:
        <div id="alert" class="alert-success hidden-xs" style="text-align: center">{{!status}}</div>
    % elif status.find("ERROR") >= 0:
        <div id="alert" class="alert-danger hidden-xs" style="text-align: center">{{!status}}</div>
    % elif status.find("WARNING") >= 0:
        <div id="alert" class="alert-warning hidden-xs" style="text-align: center">{{!status}}</div>
    % else:
        <div id="alert" class="alert-info hidden-xs" style="text-align: center">{{!status}}</div>
    % end
%end
