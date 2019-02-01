from flask import Flask, render_template, jsonify
import json
import urllib.request

import Station
import Sensor
import StationData

app = Flask(__name__)

app.debug = True


@app.route('/')
def hello_world():
    return 'AirQuality Flask App | Kamil Popczyk'


@app.route('/findAll')
def find_all():
    url_string = 'http://api.gios.gov.pl/pjp-api/rest/station/findAll'
    with urllib.request.urlopen(url_string) as url:
        json_string = str(url.read().decode())

    result = Station.station_from_dict(json.loads(json_string))
    stations_dict = {}
    for station in result:
        stations_dict[station.station_name] = station.id

    return jsonify(stations_dict)


@app.route('/station/<station_id>/sensors')
def stations_sensors_info(station_id):
    url_string = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/{}'
    with urllib.request.urlopen(url_string.format(station_id)) as url:
        json_string = str(url.read().decode())

    result = Sensor.sensor_from_dict(json.loads(json_string))
    station_sensors_info = []

    for r in result:
        station_sensors_info.append(r.param.param_name)

    return jsonify(station_sensors_info)


@app.route('/location/<station_id>')
def station_data(station_id):
    url_string = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/{}'
    with urllib.request.urlopen(url_string.format(station_id)) as url:
        json_string = str(url.read().decode())

    result = StationData.station_data_from_dict(json.loads(json_string))
    station_data_info = {}

    for r in result.values:
        station_data_info[str(r.date)] = r.value

    return jsonify(station_data_info)


if __name__ == '__main__':
    app.run()
