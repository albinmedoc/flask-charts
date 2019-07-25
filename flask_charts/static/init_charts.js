$(document).ready(function () {
  google.charts.load('current');
  google.charts.setOnLoadCallback(renderCharts);
  function renderCharts() {
    $('.chart').each(function (i, c) {
      var chart_info = JSON.parse($(this).children('.chart-info').text());
      if (chart_info.data_url) {
        $.ajax({
          type: "POST",
          dataType: "json",
          url: chart_info.data_url,
          success: function (data) {
            chart_info.data = data;
            setup_chart(chart_info);
          }
        });
      } else {
        setup_chart(chart_info);
      }
    });
  }
});

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
          google.visualization.events.addListener(wrapper.getChart(), event_listener.event, window[event_listener.function]);
        }
      });
    }
  }
}