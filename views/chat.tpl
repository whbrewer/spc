%include('header.tpl')
%include('navbar.tpl')

<div style="font-size:12pt; position:absolute; bottom:0px; left:10px; right:10px">
<div id="inbox" style="font-size:12pt">
  %for message in messages:
    %include message.tpl message=message
  %end
</div>

<form class="form-horizontal" action="/a/message/new" method="post" id="messageform">
  <div class="input-group col-xs-12">
      <input type="text" class="form-control input-lg" style="background-color:#faffbd;margin-top:10px" placeholder="enter message..." name="body" id="message"/>
      <!-- <input class="btn btn-success" type="submit" value="Post"/> -->
  </div>
</form>
</div>

%from bottle import url

<script src="{{ url("static", filename='jquery-2.1.4.min.js') }}" type="text/javascript"></script>
<script src="/static/js/chat.js" type="text/javascript"></script>

%include('footer.tpl')
