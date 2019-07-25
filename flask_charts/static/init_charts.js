window.onload = function () {
  google.charts.load('current');
  google.charts.setOnLoadCallback(renderCharts);
  function renderCharts() {
    var charts = document.getElementsByClassName("chart");
    for (var i = 0; i < charts.length; i++) {
      var chart_info = JSON.parse(charts[i].firstElementChild.innerHTML);
      if (chart_info.data_url) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4) {
            chart_info.data = JSON.parse(xhr.responseText);
            setup_chart(chart_info);
          }
        };
        xhr.open('POST', chart_info.data_url);
        xhr.send();
      } else {
        setup_chart(chart_info);
      }
    }
  }
}

function setup_chart(chart_info) {
  temp = {
    'containerId': chart_info.id,
    'chartType': chart_info.type,
    'dataTable': chart_info.data,
    'dataSourceUrl': chart_info.data_url,
    'options': chart_info.options
  };
  var wrapper = new google.visualization.ChartWrapper(temp);
  google.visualization.events.addListener(wrapper, 'ready', onReady);
  wrapper.draw();
  function onReady() {
    if (chart_info.event_listeners) {
      chart_info.event_listeners.forEach(function (event_listener) {
        if (window[event_listener.function]) {
          google.visualization.events.addListener(wrapper, event_listener.event, window[event_listener.function]);
        }
      });
    }
  }
}