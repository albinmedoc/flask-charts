var flask_charts = {};

window.onload = function () {
  google.charts.load('current');
  google.charts.setOnLoadCallback(init_charts);
  function init_charts() {
    var charts = document.getElementsByClassName("chart");
    for (var i = 0; i < charts.length; i++) {
      var chart_info = JSON.parse(charts[i].firstElementChild.innerHTML);
      setup_chart(chart_info);
    }
  }
}

function set_data(wrapper, data_url){
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      wrapper.setDataTable(JSON.parse(xhr.responseText));
      wrapper.draw();
    }
  };
  xhr.open('POST', data_url);
  xhr.send();
}

function setup_chart(chart_info) {
  temp = {
    'containerId': chart_info.id,
    'chartType': chart_info.type,
    'dataTable': chart_info.data,
    'options': chart_info.options
  };
  var wrapper = new google.visualization.ChartWrapper(temp);
  google.visualization.events.addListener(wrapper, 'ready', on_ready);
  wrapper.draw();
  if(chart_info.data_url){
    set_data(wrapper, chart_info.data_url);
    if(chart_info.refresh){
      window.setInterval(function(){
        set_data(wrapper, chart_info.data_url);
      }, chart_info.refresh);
    }
  }
  function on_ready() {
    if (chart_info.event_listeners) {
      chart_info.event_listeners.forEach(function (event_listener) {
        if (window[event_listener.function]) {
          google.visualization.events.addListener(wrapper, event_listener.event, window[event_listener.function]);
        }
      });
    }
    flask_charts[chart_info.id] = {};s
    flask_charts[chart_info.id] = wrapper;
  }
}