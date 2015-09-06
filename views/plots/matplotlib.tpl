%include('header')
%include('navbar')
%include('plots/header')

<script>
	document.getElementById("myplot").innerHTML="<img src='../{{img_path}}'/>";
</script>

%include('footer')
