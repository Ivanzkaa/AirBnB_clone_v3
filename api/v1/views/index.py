#!/usr/bin/python3
"""the route and the status"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """returning the status"""
    return jsonify({"status": "OK"}), 200


@app_views.route("/stats", strict_slashes=False)
def retrieving_stats():
    """creating an endpoint retrieving the number
    of each objects by type"""
    classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
               "reviews": "Review", "states": "State", "users": "User"}
    count_dict = {}

    for key, value in classes.items():
        count = storage.count(value)
        count_dict[key] = count
    return jsonify(count_dict), 200
