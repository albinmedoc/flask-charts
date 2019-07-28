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
### Init Flask-Charts
```python
from flask import Flask, jsonify, render_template, url_for
from flask_charts import GoogleCharts, GenericChart, ChartData

app = Flask(__name__)
charts = GoogleCharts(app)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](LICENSE)
