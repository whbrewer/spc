(function() {
    var data = JSON.parse(document.getElementById('flot-3d-data-json').textContent);
    var options = JSON.parse(document.getElementById('flot-3d-options-json').textContent);
    var zData = JSON.parse(document.getElementById('flot-3d-z-data-json').textContent);
    var zLabel = JSON.parse(document.getElementById('flot-3d-z-label-json').textContent);

    var plotParent = document.getElementById('myplot');
    plotParent.style.position = 'relative';

    var sliderParent = document.createElement('div');
    sliderParent.style.display = 'flex';
    sliderParent.style.marginBottom = '30px';

    var sliderLabel = document.createElement('div');
    sliderLabel.style.marginRight = '10px';
    sliderLabel.textContent = zLabel + ':';

    var sliderValue = document.createElement('div');
    sliderValue.style.marginRight = '10px';
    sliderValue.style.width = '50px';
    sliderValue.textContent = zData[zData.length - 1];

    var slider = document.createElement('input');
    slider.setAttribute('type', 'range');
    slider.setAttribute('max', data.length - 1);
    slider.value = data.length - 1;

    sliderParent.appendChild(sliderLabel);
    sliderParent.appendChild(sliderValue);
    sliderParent.appendChild(slider);

    options = $.extend(true, {yaxis: getYMinMax(data, options)}, options);
    data.forEach(initPlot);

    var activePlot = plotParent.children[plotParent.children.length - 1];
    activePlot.style.visibility = null;

    plotParent.parentNode.appendChild(sliderParent);

    slider.addEventListener('input', function() {
        var i = parseInt(slider.value);

        activePlot.style.visibility = 'hidden';
        plotParent.children[i].style.visibility = null;
        activePlot = plotParent.children[i];

        sliderValue.textContent = zData[i];
    });

    function getYMinMax(data, options) {
        var element = document.createElement('div');
        var min = null;
        var max = null;

        element.style.width = '10px';
        element.style.height = '1000px';

        data.forEach(function(x) {
            var plot = $.plot(element, x, options);
            var axis = plot.getYAxes()[0];

            if (min === null || axis.min < min) {
                min = axis.min;
            }

            if (max === null || axis.max > max) {
                max = axis.max;
            }
        });

        console.log('Min:', min);
        console.log('Max:', max);

        return {min: min, max: max};
    }

    function initPlot(singlePlotData) {
        var zoomed = false;

        var plotElement = document.createElement('div');
        plotElement.style.position = 'absolute';
        plotElement.style.top = '0';
        plotElement.style.left = '0';
        plotElement.style.width = '100%';
        plotElement.style.height = '100%';
        plotElement.style.visibility = 'hidden';

        plotParent.appendChild(plotElement);

        var plot = $.plot(plotElement, singlePlotData, options);

        $(plotElement).on('plotselected', function (e, ranges) {
            zoomed = true;

            var newOptions = $.extend(true, {}, options, {
                xaxis: {
                    min: ranges.xaxis.from,
                    max: ranges.xaxis.to,
                },
                yaxis: {
                    min: ranges.yaxis.from,
                    max: ranges.yaxis.to,
                },
            });

            $.plot(plotElement, singlePlotData, newOptions);
        });

        plotElement.addEventListener('dblclick', resetPlot);
        window.addEventListener('resize', resetPlot);
        slider.addEventListener('input', resetPlot);

        function resetPlot() {
            if (!zoomed) return;
            zoomed = false;

            $.plot(plotElement, singlePlotData, options);
        }
    }
}());
