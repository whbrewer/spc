%include('header.tpl')
<link rel="stylesheet" href="/static/css/chat.css">
%include('navbar.tpl')

<div id="inbox">
  %for message in messages:
    %include message.tpl message=message
  %end
</div>

<form class="form-horizontal" action="/a/message/new" method="post" id="messageform">
  <div class="input-group">
      <input type="text" class="form-control" name="body" id="message" style="width:500px"/>
      <input class="btn btn-success" type="submit" value="Post"/>
  </div>
</form>

%from bottle import url

<script src="{{ url("static", filename='jquery-2.1.4.min.js') }}" type="text/javascript"></script>
<script src="/static/js/chat.js" type="text/javascript"></script>

%include('footer.tpl')
