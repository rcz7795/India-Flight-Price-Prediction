import pickle
import json
import numpy as np
from os import path

airline_values = None
source_values = None
destination_values = None
stop_values = None
model = None

def load_saved_attributes():

    global airline_values
    global source_values
    global destination_values
    global stop_values
    global model

    with open("columns.json", "r") as f:
        resp = json.load(f)
        airline_values = resp["airlines"]
        source_values = resp["source"]
        destination_values = resp["destination"]
        stop_dict = resp["wickets"]
        stop_values = [i for i in stop_dict.keys()]

    model = pickle.load(open("flight_price_predictor.pickle", "rb"))

def get_airlines_names():
    return airline_values

def get_source_names():
    return source_values

def get_destination_names():
    return destination_values

def get_stop_names():
    return stop_values

def predict_flight_price(airline, source, dest, journey_day, journey_month, dep_hour, dep_minute, arrival_hour, arrival_minute, duration_hour, duration_minute, total_stops):
    try:
        airline_index = airline_values.index(airline)
        source_index = source_values.index(source)
        destination_index = destination_values.index(dest)
        stop_index = stop_values.index(total_stops)
    except:
        airline_index = -1
        source_index = -1
        destination_index = -1
        stop_index = -1

    airline_array = np.zeros(len(airline_values))
    if airline_index >= 0:
        airline_array[airline_index] = 1

    source_array = np.zeros(len(source_values))
    if source_index >= 0:
        source_array[source_index] = 1

    destination_array = np.zeros(len(destination_values))
    if destination_index >= 0:
        destination_array[destination_index] = 1

    airline_array = airline_array[:-1]
    source_array = source_array[:-1]
    destination_array = destination_array[:-1]

    sample = np.concatenate((airline_array, source_array, destination_array, np.array([journey_day, journey_month, dep_hour, dep_minute, arrival_hour, arrival_minute, duration_hour, duration_minute, stop_index])))

    return model.predict(sample.reshape(1,-1))[0]


if __name__ == '__main__':
    load_saved_attributes()
else:
    load_saved_attributes()
