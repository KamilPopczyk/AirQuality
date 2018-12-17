from flask import Flask, render_template, jsonify
import json
import urllib.request

app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return 'AirQuality'

@app.route('/findAll')
def find_all():
    url = 'http://api.gios.gov.pl/pjp-api/rest/station/findAll'
    with urllib.request.urlopen(url) as url:
        stations_list = json.loads(url.read().decode())

    stations_dict = {}
    for station in stations_list:
        stations_dict[station['stationName']] = station['id']

    return jsonify(stations_dict)

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
