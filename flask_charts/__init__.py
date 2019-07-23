import json
import string
from jinja2 import Markup, Environment, PackageLoader
import pkg_resources
import flask
from .utils import render_data, prep_data

class GenericChart(object):

    def __init__(self, type_, id_, options=None, data_url=None):
        self.id = id_
        self.type = type_
        self.options = options
        self.data_url = data_url
        self.event_listeners = []

        self._columns = []
        self._rows = []

        if(not isinstance(self.id, str)):
            raise TypeError("id must be type str, not {}".format(type(self.id)))
        if(self.id.isdigit()):
            raise ValueError("id can´t be a number")
        if(not self.id):
            raise ValueError("id must contain at least one character.")
        if(" " in self.id):
            raise ValueError("id may not contain spaces; they are not supported in id values in HTML5.")
        if(not ord(self.id[0]) < 128):
            raise ValueError("id must start with a letter as it is used as a JavaScript variable name")
        if(self.type not in ["AnnotationChart", "AreaChart", "BarChart", "BubbleChart", "CalendarChart", "CandlestickChart", "ColumnChart", "ComboChart", "GanttChart", "GaugeChart", "GeoChart", "Histogram", "LineChart", "Map", "OrgChart", "PieChart", "Sankey", "ScatterChart"]):
            raise ValueError("{} is not a valid Chart type or it´s not implemented.".format(self.type))
        
    def add_event_listener(self, event, function_name):
        self.event_listeners.append({
            "event": event,
            "function": function_name
        })

    def add_column(self, type_, label=""):
        if isinstance(label, str) and isinstance(type_, str):
            if type_ in ["boolean", "date", "datetime", "number", "string", "timeofday"]:
                self._columns.append((type_, label))
            else:
                raise ValueError("{} is not a valid column type".format(type_))
        else:
            raise TypeError("type_ and label must be strings")

    def add_rows(self, rows):
        if isinstance(rows, list):
            self._rows += rows
        else:
            raise TypeError("rows must be type list, not {}".format(type(rows)))

    @property
    def data_json(self):
        return json.dumps(render_data(self._columns, self._rows))

    @property
    def options_json(self):
        return json.dumps(self.options)
    
    def __call__(self):
        return Markup(Environment(loader=PackageLoader("flask_charts", "templates")).get_template("chart.html").render(chart=self))

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

def ChartData(data):
    if(not isinstance(data, dict)):
        TypeError("data must be a dict")
    return flask.jsonify(prep_data(data))