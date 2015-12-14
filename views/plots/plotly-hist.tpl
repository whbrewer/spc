% rebase('plots/plotly-base.tpl')

<div id="myplot" style="width:600px;height:250px;"></div>

<script>
var trace1 = {
  x: {{!data}},
  type: 'histogram',
  marker: {
    color: 'rgb(158,202,225)',
    opacity: 0.6,
    line: {
      color: 'rbg(8,48,107)',
      width: 1.5
    }
  }
};

var data = [trace1];

var layout = {
  title: 'Allele Frequency Distribution',
  xaxis: {
    title: 'Fraction of Population',
    titlefont: {
      size: 18,
      color: '#7f7f7f'
    }
  },
  yaxis: {
    title: 'Frequency',
    titlefont: {
      size: 18,
      color: '#7f7f7f'
    }
  }
};

myplot = document.getElementById('myplot')
Plotly.newPlot(myplot, data, layout)

window.onresize = function() {
  Plotly.Plots.resize(myplot)
};

</script>

