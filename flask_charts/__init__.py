# -*- coding: utf-8
import json
import string
from jinja2 import Markup, Environment, PackageLoader
import pkg_resources
import flask
from .utils import render_data, prep_data

class GenericChart(object):

    def __init__(self, type_, id_, options=None, data_url=None, refresh=None):
        self.id = id_
        self.type = type_
        self.options = options
        self.refresh = refresh
        self.data = ChartData()
        self.data_url = data_url
        self.event_listeners = []

        if(not isinstance(self.id, str)):
            raise TypeError("id must be type str, not {}".format(type(self.id)))
        if(self.id.isdigit()):
            raise ValueError("id can´t be a number")
        if(not self.id):
            raise ValueError("id must contain at least one character.")
        if(" " in self.id):
            raise ValueError("id may not contain spaces; they are not supported in id values in HTML5.")
        if(self.id[0] not in string.ascii_letters):
            raise ValueError("id must start with a letter as it is used as a JavaScript variable name")
        if(self.type not in ["AnnotationChart", "AreaChart", "BarChart", "BubbleChart", "CalendarChart", "CandlestickChart", "ColumnChart", "ComboChart", "GanttChart", "GaugeChart", "GeoChart", "Histogram", "LineChart", "Map", "OrgChart", "PieChart", "Sankey", "ScatterChart"]):
            raise ValueError("{} is not a valid Chart type or it´s not implemented.".format(self.type))
        
    def add_event_listener(self, event, function_name):
        self.event_listeners.append({
            "event": event,
            "function": function_name
        })

    def get_json(self):
        temp = {}
        temp["id"] = self.id
        temp["type"] = self.type
        temp["options"] = self.options
        if(self.refresh is not None):
            temp["refresh"] = self.refresh
        if(self.data):
            temp["data"] = self.data.to_json()
        elif(self.data_url is not None):
            temp["data_url"] = self.data_url
        if(self.event_listeners):
            temp["event_listeners"] = self.event_listeners
        return json.dumps(temp)
    
    def __call__(self):
        #Make sure either data or data_url is set
        if(not self.data and not self.data_url):
            raise Warning("Chart´s data or data_url must be set to render the chart")
        return Markup(Environment(loader=PackageLoader("flask_charts", "templates")).get_template("chart.html").render(id=self.id, json=self.get_json()))

class GoogleCharts(object):
    def __init__(self, app=None):

        self.app = app
        self.config = None

        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        """Initializes the extension against the app"""
        if isinstance(app, flask.Flask):
            self.app = app
            self.app.context_processor(self.template_variables)
            self.app.add_url_rule("/init_charts.js", "init_charts", self._init_charts)
            return True
        raise TypeError("app must be type flask.Flask, not {}".format(type(app)))

    def template_variables(self):
        return {'init_charts': Markup("<script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script><script type='text/javascript' src='/init_charts.js'></script>")}
    
    def _init_charts(self):
        return flask.send_file(pkg_resources.resource_stream("flask_charts", "static/init_charts.js"),
                               attachment_filename="init_charts.js")

class ChartData():
    def __init__(self):
        self._columns = []
        self._rows = []
    
    def add_column(self, type_, label=""):
        if isinstance(label, str) and isinstance(type_, str):
            if type_ in ["boolean", "date", "datetime", "number", "string", "timeofday"]:
                self._columns.append((type_, label))
            else:
                raise ValueError("{} is not a valid column type".format(type_))
        else:
            raise TypeError("type_ and label must be strings")
    
    def add_row(self, row):
        if isinstance(row, list):
            self._rows.append(row)
        else:
            raise TypeError("row must be type list, not {}".format(type(row)))
    
    # For python < 3.0
    def __nonzero__(self):
        return len(self._columns) > 0 and len(self._rows) > 0
    
    # For python => 3.0
    def __bool__(self):
        return len(self._columns) > 0 and len(self._rows) > 0
    
    def to_json(self):
        return json.dumps(render_data(self._columns, self._rows))

    def data(self):
        return render_data(self._columns, self._rows)