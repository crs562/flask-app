import json
import requests

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
    
if __name__ == '__main__':
    app.run()
