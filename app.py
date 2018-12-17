from flask import Flask, render_template, jsonify, request
import json
import urllib.request

app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return 'AirQuality'


@app.route('/location/<station_id>')
def station_page(station_id):
    url = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/{}'
    url_getData = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/{}'

    with urllib.request.urlopen(url.format(station_id)) as url:
        sensors_data = json.loads(url.read().decode())

    print(sensors_data[0]['param']['paramName'])
    print(sensors_data[0]['id'])

    air_data = {}

    for sensor in sensors_data:
        with urllib.request.urlopen(url_getData.format(sensor['id'])) as url:
            param_data = json.loads(url.read().decode())
        air_data[sensor['param']['paramCode']] = param_data['values']
        # air_data = {sensor}

    return jsonify(air_data)

if __name__ == '__main__':
    app.run()
