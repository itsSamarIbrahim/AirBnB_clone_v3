#!/usr/bin/python3
"""
Definition of the API server
"""

from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS(app)  # Enable CORS for the entire app
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors that returns a JSON response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
