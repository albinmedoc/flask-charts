from __future__ import with_statement

import json
import sys
import datetime

from flask import Flask
from jinja2 import Markup
from flask_charts import GoogleCharts, GenericChart, ChartData

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestGoogleCharts(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.debug = True
        self.charts = GoogleCharts(app)
        self.app = app
        self.client = app.test_client()
    
    def tearDown(self):
        self.app = None

    def test(self):
        self.assertTrue("renderCharts()" in self.client.get("/init_charts.js").data.decode("utf8"))


    def test_init_app(self):
        with self.assertRaises(TypeError):
            self.charts.init_app(1)


class TestGenericChart(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.debug = True
        self.charts = GoogleCharts(app)
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        self.app = None

    def test_init(self):
        with self.assertRaises(ValueError):
            chart = GenericChart("PieChart", "")
        with self.assertRaises(ValueError):
            GenericChart("PieChart", "A B")
        with self.assertRaises(ValueError):
            GenericChart("PieChart", "3")
        with self.assertRaises(TypeError):
            chart = GenericChart(1)
        with self.assertRaises(ValueError):
            chart = GenericChart("BananaChart", "chart")
        with self.assertRaises(ValueError):
            chart = GenericChart("PieChart", "!chart")
        with self.assertRaises(TypeError):
            chart = GenericChart("PieChart", 123)
    
    def test_addEventListener(self):
        chart = GenericChart("PieChart", "test")
        chart.add_event_listener("ready", "my_function")
        assert chart.event_listeners[0]["event"] == "ready" and chart.event_listeners[0]["function"] == "my_function"
    
    def test_getJson(self):
        chart = GenericChart("PieChart", "test", options={"title": "chart"}, data_url="/data")
        chart.add_event_listener("ready", "my_function")
        self.assertTrue(chart.get_json() == json.dumps({
                                                        "id": "test",
                                                        "type": "PieChart",
                                                        "options": {"title": "chart"},
                                                        "data_url": "/data",
                                                        "event_listeners": [{
                                                                            "event": "ready",
                                                                            "function": "my_function"
                                                                            }]
                                                        }))
        chart.data.add_column("string", "col")
        chart.data.add_row(["test", 200])
        self.assertTrue(chart.get_json() == json.dumps({
                                                        "id": "test",
                                                        "type": "PieChart",
                                                        "options": {"title": "chart"},
                                                        "data": chart.data.to_json(),
                                                        "event_listeners": [{
                                                                            "event": "ready",
                                                                            "function": "my_function"
                                                                            }]
                                                        }))
    
    def test_render(self):
        chart = GenericChart("PieChart", "test")
        with self.assertRaises(Warning):
            chart()
        chart.data.add_column("string", "col")
        with self.assertRaises(Warning):
            chart()
        chart.data.add_row(["test", 200])
        self.assertTrue(isinstance(chart(), Markup))



class TestChartData(unittest.TestCase):
    def test_addColumn(self):
        data = ChartData()
        data.add_column("string", "col")
        assert data._columns[0][0] == "string" and data._columns[0][1] == "col"
        with self.assertRaises(ValueError):
            data.add_column("", "")
        with self.assertRaises(TypeError):
            data.add_column(1)
    
    def test_addRow(self):
        data = ChartData()
        data.add_row(["test", 200])
        assert data._rows[0][0] == "test" and data._rows[0][1] == 200
        with self.assertRaises(TypeError):
            data.add_row("row")

        data.add_row([datetime.datetime(2019, 1, 1, 1, 1, 1, 1), datetime.date(2019, 1, 1)])
        json_data = json.loads(data.to_json())
        assert json_data["rows"][1]["c"][0]["v"] == "Date(2019, 0, 1, 1, 1, 1, 1)" and json_data["rows"][1]["c"][1]["v"] == "Date(2019, 0, 1)"

    def test_bool(self):
        data = ChartData()
        self.assertFalse(data)
        data.add_column("string", "col")
        self.assertFalse(data)
        data.add_row(["test", 200])
        self.assertTrue(data)

if __name__ == "__main__":
    unittest.main()