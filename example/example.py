from flask import Flask, jsonify, render_template, url_for
from flask_charts import GoogleCharts, Chart, ChartData
from random import randint

app = Flask(__name__)
charts = GoogleCharts(app)

@app.route("/")
def index():
    pizza_chart = Chart("PieChart", "pizza")

    pizza_chart.options = {
                            "title": "Pizzas eaten",
                            "is3D": True,
                            "width": 500,
                            "height": 500
                          }

    pizza_chart.data.add_column("string", "Person")
    pizza_chart.data.add_column("number", "Count")
    pizza_chart.data.add_row(["Albin", 3])
    pizza_chart.data.add_row(["Robert", 4])
    pizza_chart.data.add_row(["Daniel", 2.5])
    pizza_chart.add_event_listener("select", "my_function")
                                                                                                                      # Refreshes every second
    random_chart = Chart("PieChart", "random_chart", options= {"title": "Random values"}, data_url=url_for("data"), refresh=1000)
    return render_template("example.html", pizza_chart=pizza_chart, random_chart=random_chart)

@app.route("/data", methods=["POST"])
def data():
    data = ChartData()
    data.add_column("string", "Person")
    data.add_column("number", "Count")

    data.add_row(["Ben", randint(1, 100)])
    data.add_row(["Julia", randint(1, 100)])
    data.add_row(["George", randint(1, 100)])

    return jsonify(data.data())

if __name__ == "__main__":
    app.run(debug=True)