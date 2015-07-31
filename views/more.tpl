%include('header')

<div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
    <h4 class="modal-title" id="myModalLabel">Filename is: {{fn}}</h4>       
</div>

%include('more_contents')

<div class="modal-footer">
   <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
</div>

%include('footer')
