from flask import Flask, render_template, jsonify

app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return 'AirQuality'


@app.route('/<station>', methods=['GET'])
def station_page():
    url = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/'


if __name__ == '__main__':
    app.run()
