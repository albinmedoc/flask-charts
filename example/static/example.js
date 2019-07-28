// Select event (runs when user selects a value in chart)
function my_function(e){
    var chart = flask_charts["pizza"]["chart"].getChart();

    // Retrieves the charts data (rows and columns)
    var chart_data = flask_charts["pizza"]["data"];

    // Retrieves the row that the user clicked
    var selected_row = chart_data["rows"][chart.getSelection()[0]["row"]]["c"];

    // Retrieves the person's name which is the first value in the list
    var person_clicked = selected_row[0]["v"];

    // Retrieves the person's pizza count which is the second value in the list
    var pizza_count = selected_row[1]["v"];

    alert(person_clicked + " ate " + pizza_count + " pizzas.");

    // Removes the selection so the user can click the same value in chart to get information
    chart.setSelection(null);
}