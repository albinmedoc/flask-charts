import json
import string
from jinja2 import Markup, Environment, PackageLoader
import pkg_resources
import flask
from .utils import render_data, prep_data

class GenericChart(object):

    def __init__(self, id_, type_, options=None, data_url=None):
        self.id = id_
        self.type = type_
        self.options = options
        self.data_url = data_url
        self.event_listeners = []

        self._columns = []
        self._rows = []

        if(not isinstance(self.id, str)):
            raise TypeError("id must be type str, not {}", type(self.id))
        if(not self.id):
            raise ValueError("id must contain at least one character.")
        if(" " in self.id):
            raise ValueError("id may not contain spaces; they are not supported in id values in HTML5.")
        if(not ord(self.id[0]) < 128):
            raise ValueError("id must start with a letter as it is used as a JavaScript variable name")
        
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


class AnnotationChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "AnnotationChart", options=options, data_url=data_url)


class AreaChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "AreaChart", options=options, data_url=data_url)


class BarChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "BarChart", options=options, data_url=data_url)


class BubbleChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "BubbleChart", options=options, data_url=data_url)


class CalendarChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "Calendar", options=options, data_url=data_url)


class CandlestickChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "CandlestickChart", options=options, data_url=data_url)


class ColumnChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "ColumnChart", options=options, data_url=data_url)


class ComboChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "ComboChart", options=options, data_url=data_url)

class DiffChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        raise NotImplementedError("DiffChart is not yet available in Flask-Charts")


class GanttChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "Gantt", options=options, data_url=data_url)


class GaugeChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "Gauge", options=options, data_url=data_url)


class GeoChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "GeoChart", options=options, data_url=data_url)


class Histogram(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "Histogram", options=options, data_url=data_url)


class LineChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "LineChart", options=options, data_url=data_url)


class Map(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "Map", options=options, data_url=data_url)


class OrgChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "OrgChart", options=options, data_url=data_url)


class PieChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "PieChart", options=options, data_url=data_url)


class Sankey(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "Sankey", options=options, data_url=data_url)


class ScatterChart(GenericChart):
    def __init__(self, id_, options=None, data_url=None):
        super().__init__(id_, "ScatterChart", options=options, data_url=data_url)

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
        return {'charts_init': Markup("<script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script><script type='text/javascript' src='/init_charts.js'></script>")}
    
    def _init_charts(self):
        return flask.send_file(pkg_resources.resource_stream("flask_charts", "static/init_charts.js"),
                               attachment_filename="init_charts.js")

def ChartData(data):
    if(not isinstance(data, dict)):
        TypeError("data must be a dict")
    return flask.jsonify(prep_data(data))