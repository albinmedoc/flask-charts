from flask import Flask, jsonify, render_template, url_for
from flask_charts import GoogleCharts, GenericChart, ChartData

app = Flask(__name__)
charts = GoogleCharts(app)

@app.route("/")
def index():
    pizza_chart = GenericChart("PieChart", "pizza")

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

    url_chart = GenericChart("PieChart", "url_chart", options= {"title": "Pizzas eaten #2"}, data_url=url_for("data"))
    return render_template("example.html", pizza_chart=pizza_chart, url_chart=url_chart)

@app.route("/data", methods=["GET"])
def data():
    data = ChartData()
    data.add_column("string", "Person")
    data.add_column("number", "Count")

    data.add_row(["Ben", 4])
    data.add_row(["Julia", 2])
    data.add_row(["George", 3.5])

    return jsonify(data.data())

if __name__ == "__main__":
    app.run(debug=True)