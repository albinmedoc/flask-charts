from __future__ import with_statement

import json
import sys

from flask import Flask
from flask_charts import GoogleCharts, GenericChart

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


class TestGenericCharts(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.debug = True
        self.charts = GoogleCharts(app)
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        self.app = None

    def test_addColumn(self):
        chart = GenericChart("PieChart", "test")
        chart.add_column("string", "col")
        assert chart._columns[0][0] == "string" and chart._columns[0][1] == "col"
        with self.assertRaises(ValueError):
            chart.add_column("", "")
        with self.assertRaises(TypeError):
            chart.add_column(1)

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
        #Add tests for chart type

if __name__ == "__main__":
    unittest.main()