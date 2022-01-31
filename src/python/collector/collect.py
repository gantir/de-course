import base64
import json
import logging
import urllib
from datetime import datetime

from flask import Flask
from flask import request, make_response, redirect as flask_redirect

__version__ = '1.0.0'

app = Flask(__name__)

def request_log(request):
    params = {}
    if request.method == 'GET':
        params = request.values.to_dict(flat=False)
    elif request.method == 'POST':
        if request.is_json:
            params = request.get_json()
        else:
            params = urllib.parse.parse_qs(request.data)

    log = {
        "type": "collect",
        "collector_tstamp": datetime.now().timestamp(),
        "v_collector": __version__,
        "request_url": request.url,
        "headers": dict(request.headers),
        "cookies": request.cookies,
        "params": params,
    }

    logging.info(json.dumps(log))

def generate_pixel():
    pixel = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    pixel = base64.b64decode(pixel)
    response = make_response(pixel)
    response.headers['Content-Type'] = 'image/gif'
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "GET, POST"
    response.headers['Cache-Control'] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers['Cache-Control'] = "post-check=0, pre-check=0"
    response.headers['Pragma'] = "no-cache"

    return response

def handle_cors():
    return make_response("", 204)

@app.route('/c', methods=['GET', 'POST', 'OPTIONS'])
def pixel():
    if request.method == "OPTIONS":
        return handle_cors()

    response = generate_pixel()

    request_log(request)

    return response

@app.route('/r', methods=['GET'])
def redirect():
    request_log(request)

    return flask_redirect(request.values.get("u"), code=302)