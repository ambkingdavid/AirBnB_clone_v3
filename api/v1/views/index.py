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


# Create a route '/stats' on the app_views object that
# returns the count of each object type
@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Retrieves the number of each objects
    """
    objs = {
            "amenities": storage.count(Amenities),
            "cities": storage.count(Cities),
            "places": storage.count(Place),
            "reviews": storage.count(Reviews),
            "states": storage.count(States),
            "users": storage.count(Users)
            }
    return jsonify(objs)
