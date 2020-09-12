from flask import Flask, request, render_template, jsonify
from flask_cors import cross_origin

import FlightPricePredictor as tm

app = Flask(__name__)

@app.route('/get_airlines_names', methods=['GET'])
def get_airlines_names():
    response = jsonify({
        'airlines': tm.get_airlines_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_source_names', methods=['GET'])
def get_source_names():
    response = jsonify({
        'source': tm.get_source_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_destination_names', methods=['GET'])
def get_destination_names():
    response = jsonify({
        'destination': tm.get_destination_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_stop_names', methods=['GET'])
def get_stop_names():
    response = jsonify({
        'stop': tm.get_stop_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_wickets_names', methods=['GET'])
def get_wickets_names():
    response = jsonify({
        'wickets': tm.get_wickets_values()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
#@cross_origin()
def predict():
    if request.method == "POST":
        source = request.form.get('source')
        dest = request.form.get('destination')
        airline = request.form.get('airlines')
        doj = request.form.get('doj')
        dt = request.form.get('dt')
        at = request.form.get('at')
        total_stops = request.form.get('stop')

        journey_day = int(doj.split('-')[2])
        journey_month = int(doj.split('-')[1])
        dep_hour = int(dt.split(':')[0])
        dep_minute = int(dt.split(':')[1])
        arrival_hour = int(at.split(':')[0])
        arrival_minute = int(at.split(':')[1])
        if arrival_hour >= dep_hour:
            duration_hour = arrival_hour - dep_hour
        else:
            duration_hour = arrival_hour - dep_hour + 24
        duration_minute = arrival_minute - dep_minute
        if duration_minute < 0:
            duration_minute = duration_minute + 60
            duration_hour = duration_hour - 1
        
        prediction = round(float(tm.predict_flight_price(airline, source, dest, journey_day, journey_month, dep_hour, dep_minute, arrival_hour, arrival_minute, duration_hour, duration_minute, total_stops)), 2)

        return render_template("index.html", prediction_text="The estimated flight fare is Rs: " + str(prediction))

    return render_template("index.html")


if __name__ == "__main__":
    tm.load_saved_attributes()
    app.run(debug = True)