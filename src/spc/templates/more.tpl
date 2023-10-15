%rebase('base.tpl')
%include('navactions')

<h4>{{fn}}</h4>

<div class="bs-example">
	<input id="searchbox" type="text" class="form-control input-lg"
		   onchange="show(this.value)" placeholder="Search...">
</div>

%include('more_contents')

<button style="position:fixed; bottom:200px; right:-5px" class="cd-top btn btn-primary" onclick="addLineNumbers()"><span class="glyphicon glyphicon-list"></span></button>

<button style="position:fixed; bottom:145px; right:-5px" class="cd-top btn btn-primary" onclick="scrollToTop()"><span class="glyphicon glyphicon-menu-up"></span></button>

<button style="position:fixed; bottom:100px; right:-5px" class="cd-top btn btn-primary" onclick="scrollToBottom()"><span class="glyphicon glyphicon-menu-down"></span></button>

<div class="col-xs-12" style="height:5px"></div>

<script>

	function show(str) {
		$("pre").highlight(str);
		window.find(str);
	}

	function scrollToTop() {
		$('html, body').animate({scrollTop: 0}, 500, 'linear');
	}

	function scrollToBottom() {
		$('html, body').animate({scrollTop: $(document).height()}, 500, 'linear');
	}

	function scrollUp() {
		$('html, body').animate({scrollTop: '-=100'}, 500, 'linear');
	}

	function scrollDown() {
		$('html, body').animate({scrollTop: '+=100'}, 500, 'linear');
	}

	function addLineNumbers() {
		$('pre').html('<table>'+$.map($('pre').text().split('\n'), function(t, i){
			return '<tr><td style="color:maroon">'+(i+1)+'</td><td>'+t+'</td></tr>';
		}).join('')+'</table>');
	}

	$(document).ready(function(){

	    document.onkeyup = KeyCheck;

	    function KeyCheck(e) {

	    	// custom mendel code -- prepare following for removal
			// $("pre").highlight("POLYGENIC BENEFICIALS SUMMARY");
			// $("pre").highlight("First_inst_gen, Last_inst_gen, Fix_gen, Total_inst");

	    	var KeyID = (window.event) ? event.keyCode : e.keyCode;

	    	if(e.keyCode == 71 && e.ctrlKey) { // ctrl-g cancel highlights
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
