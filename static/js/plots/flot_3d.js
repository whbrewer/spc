(function() {
    var data = JSON.parse(document.getElementById('flot-3d-data-json').textContent);
    var options = JSON.parse(document.getElementById('flot-3d-options-json').textContent);
    var zData = JSON.parse(document.getElementById('flot-3d-z-data-json').textContent);
    var zLabel = JSON.parse(document.getElementById('flot-3d-z-label-json').textContent);

    var plotParent = document.getElementById('myplot');
    plotParent.style.position = 'relative';

    data.forEach(function(singlePlotData) {
        var plotElement = document.createElement('div');
        plotElement.style.position = 'absolute';
        plotElement.style.top = '0';
        plotElement.style.left = '0';
        plotElement.style.width = '100%';
        plotElement.style.height = '100%';
        plotElement.style.visibility = 'hidden';

        plotParent.appendChild(plotElement);

        var plot = $.plot(plotElement, singlePlotData, options);
    });

    var activePlot = plotParent.children[plotParent.children.length - 1];
    activePlot.style.visibility = null;

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
    plotParent.parentNode.appendChild(sliderParent);

    slider.addEventListener('input', function() {
        var i = parseInt(slider.value);

        activePlot.style.visibility = 'hidden';
        plotParent.children[i].style.visibility = null;
        activePlot = plotParent.children[i];

        sliderValue.textContent = zData[i];
    });
}());
