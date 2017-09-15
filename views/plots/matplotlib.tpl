%rebase('base.tpl')

%include('plots/plot_list')

<script>
	document.getElementById("myplot").innerHTML="<img src='../{{img_path}}'/>";
</script>
