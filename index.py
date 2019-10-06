import json
import requests
import logging

from flask import Flask, render_template, request, jsonify
from flask import request

app = Flask(__name__)

with open('data.json') as f:
    data = json.load(f)
keys = list(data[0].keys())
keys.append("Threat")
ranges = list(range(len(data)))
API_URL = "https://us-central1-retail-use-case.cloudfunctions.net/threat_alert"

@app.route('/')
def index():
    return render_template('index.html', data=data, keys=keys, ranges=ranges)

@app.route('/update', methods=["POST"])
def update():
    thread = request.form.get("threat")
    data[0].update({"Threat": thread})
    updateData = json.dumps(data)
    with open('updateData.json', 'w') as outfile:
        json.dump(updateData, outfile)
    response = requests.post(API_URL, updateData)
    print(response.json)
    return updateData

@app.route('/api-data')
def restAPI():
    with open('updateData.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
