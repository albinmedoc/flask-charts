# Flask-Charts

[![Build Status](https://travis-ci.com/albinmedoc/flask-charts.svg?token=4GyhcjtfvUszyhA5DD7J&branch=master)](https://travis-ci.com/albinmedoc/flask-charts)
[![codecov](https://codecov.io/gh/albinmedoc/flask-charts/branch/master/graph/badge.svg?token=puiuyNKZuh)](https://codecov.io/gh/albinmedoc/flask-charts)
[![PyPI version](https://badge.fury.io/py/Flask-Charts.svg)](https://badge.fury.io/py/Flask-Charts)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/albinmedoc/flask-charts)

Flask-Charts is a Flask extension for dealing with chart visualization. Flask-Charts is using [Google Charts](https://developers.google.com/chart/) to render charts on the client-side.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Flask-Charts.

```bash
pip install Flask-Charts
```

## Usage

### Setup
Google charts are controlled through a **GoogleCharts** instance
```python
from flask import Flask
from flask_charts import GoogleCharts

app = Flask(__name__)
charts = GoogleCharts(app)
```
You can also set up the GoogleCharts instance later using the **init_app** method
```python
charts = GoogleCharts()

app = Flask(__name__)
charts.init_app(app)
```

### Creating Charts
Import Chart and declare it in your view, give it a type and id at a minimum
```python
from flask_charts import Chart

my_chart = Chart("PieChart", "my_chart")
```

#### Adding Data to a Chart
You can populate the chart using the **addColumn** and **addRows** methods on the chart.data
```python
my_chart.data.add_column("string", "Person")
my_chart.data.add_column("number", "Count")
my_chart.data.add_row(["Albin", 3])
my_chart.data.add_row(["Robert", 4])
my_chart.data.add_row(["Daniel", 2.5])
```
If you will be pulling JSON data from another endpoint, just specify the url in the **data_url** variable
```python
my_chart.data_url = url_for("data"))
```

#### Auto refresh chart data
If you are pulling data from an url you can specify how often the data will refresh
```python
my_chart.refresh = 5000 # 5 seconds interval
```

#### Adding Event Handlers to a chart
In python you have to select a event type and a javascript callback function
```python
my_chart.add_event_listener("select", "my_function")
```
In the callback function you can do whatever you want
```javascript
function my_function(){
    alert("You selected a value in the chart");
}
```

### Including Charts in Templates
Create your chart and send it to the template
```python
...
return render_template("index.html", my_chart=my_chart)
```
On every page where there will be charts, you must include **{{ init_charts }}**.
```html
<head>
    <meta charset="UTF-8">
    <title>Flask-Charts Example</title>
    {{ init_charts }}
</head>
```
To display the chart, you need to call the template variable you assign the chart to
```html
<body>
{{ my_chart() }}
</body>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](LICENSE)
