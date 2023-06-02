#!/usr/bin/python3

"""
contains the end route status
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def show_status():
    """
    shows the status
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def count_classes():
    """
    Counts the numbers of objects owned by a class
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")
                    })
