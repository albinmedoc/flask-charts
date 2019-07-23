from flask import Flask, jsonify, render_template, url_for
from flask_charts import GoogleCharts, GenericChart

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
    pizza_chart.add_column("string", "Person")
    pizza_chart.add_column("number", "Count")
    pizza_chart.add_rows([
                            ["Albin", 3],
                            ["Robert", 4],
                            ["Daniel", 2.5]
                        ])
    return render_template("example.html", pizza_chart=pizza_chart)

if __name__ == "__main__":
    app.run(debug=True)