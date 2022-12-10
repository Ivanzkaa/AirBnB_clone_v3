#!/usr/bin/python3
"""the main flask app"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)

CORS(app, resources={r"/*": {"origins": '0.0.0.0'}})


@app.teardown_appcontext
def closing_sesh(self):
    """closing the session of the
    request"""
    storage.close()


if (__name__ == "__main__"):
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if not host:
        host = '0.0.0.0'
    elif not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
