#!/usr/bin/python3
"""module for the city file"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=['Get'], strict_slashes=False)
def retrieving_amenities():
    """retrieving the list of the amenities"""
    amenity_list = []
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def retrieve_amenity(amenity_id):
    """retrieving the amenity id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def deleting_amenity(amenity_id):
    """deleting a state"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", mehtods=['POST'], strict_slashes=False)
def creating_amenity():
    """creating amenities"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if post_data.get("name") is None:
        abort(400, "Missing name")
    new_amenity = Amenity(**post_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updating the amenity"""
    keys_ignored = ['id', 'created_at', 'updated_at']
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(404, "Not a JSON")
    for key, value in put_data.items():
        if key in keys_ignored:
            pass
        else:
            setattr(city, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
