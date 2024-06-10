#!/usr/bin/python3
"""
Definition of the API server
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)

