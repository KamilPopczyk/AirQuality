from flask import Flask, render_template, jsonify
import json
import urllib.request

import Station, Sensor

app = Flask(__name__)

app.debug = True


@app.route('/')
def hello_world():
    return 'AirQuality Flask App'


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
def station_page(station_id):
    url = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/{}'
    url_getData = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/{}'
    air_data = {}

    with urllib.request.urlopen(url.format(station_id)) as url:
        sensors_data = json.loads(url.read().decode())

    for sensor in sensors_data:
        with urllib.request.urlopen(url_getData.format(sensor['id'])) as url:
            param_data = json.loads(url.read().decode())
        air_data[sensor['param']['paramCode']] = param_data['values']

    return jsonify(air_data)


if __name__ == '__main__':
    app.run()
