% messages = app.get_flashed_messages()
% if messages:
    <div id="flash_messages">
        <ul>
            % for m in messages:
            <li>{{ m[0] }}</li>
            % end
        </ul>
    </div>
% end
