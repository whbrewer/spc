%include('header')
%include('navbar')
%include('navactions')

<h4>{{fn}}</h4>

<div class="bs-example">
	<input id="searchbox" type="text" class="form-control input-lg"
		   onchange="show(this.value)" placeholder="Search...">
</div>

%include('more_contents')

<a style="position:fixed; bottom:100px; right:-5px" href="javascript:scrollToBottom()" id="bottom_btn" class="cd-top btn btn-primary"><span class="glyphicon glyphicon-menu-down"></span></a>

<a style="position:fixed; bottom:145px; right:-5px" href="javascript:scrollToTop()" id="top_btn" class="cd-top btn btn-primary"><span class="glyphicon glyphicon-menu-up"></span></a>

<div class="col-xs-12" style="height:5px"></div>

<script>

	function show(str) {
		$("pre").highlight(str);
		window.find(str);
	}

	function scrollToTop() {
		offset = $('body').offset();
		$('html, body').animate({scrollTop: offset.top}, 500, 'linear');
	}

	function scrollToBottom() {
		$('html, body').animate({scrollTop: $(document).height()}, 500, 'linear');
	}

	$(document).ready(function(){

	    document.onkeyup = KeyCheck;

	    function KeyCheck(e) {

	    	// custom mendel code -- prepare following for removal
			// $("pre").highlight("POLYGENIC BENEFICIALS SUMMARY");
			// $("pre").highlight("First_inst_gen, Last_inst_gen, Fix_gen, Total_inst");

	    	var KeyID = (window.event) ? event.keyCode : e.keyCode;

	    	if(e.keyCode == 71 && e.ctrlKey) { // ctrl-n next
				$("pre").unhighlight();
	    	}

	    	if(e.keyCode == 78 && e.ctrlKey) { // ctrl-n next
	    		str = document.getElementById('searchbox').value;
				window.find(str);
	    	}

	        if(e.keyCode == 80 && e.ctrlKey) { // ctrl-p previous
	    		str = document.getElementById('searchbox').value;
				window.find(str,false,true);
	    	}

		    // make focus search box when clicking "/" button
	    	if (e.keyCode == 191) {
				document.getElementById('searchbox').focus();
			}
	    }
	});
</script>

%include('footer')
