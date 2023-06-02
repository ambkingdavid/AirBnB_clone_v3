#!/usr/bin/python3
"""
contains the end route status
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


# Create a route '/status' on the app_views object that returns a JSON response
@app_views.route('/status', methods=['GET'])
def get_status():
    """
    shows the status
    """
    return jsonify({"status": "OK"})
