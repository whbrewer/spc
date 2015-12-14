% rebase('plots/plotly-base.tpl')

<div id="myplot" style="width:600px;height:250px;"></div>

<script>
var x = [];
for (var i = 0; i < 500; i ++) {
   x[i] = Math.random();
}

var data = [
  {
    x: x,
    type: 'histogram'
  }
];
Plotly.newPlot('myplot', data);
</script>

