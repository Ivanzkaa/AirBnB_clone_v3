#!/usr/bin/python3
"""module for the city file"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['Get'], strict_slashes=False)
def retrieving_cities(state_id):
    """retrieving the list of the cities"""
    city_list = []
    check_city = storage.get("State", state_id)
    if check_city is None:
        abort(404)
    cities = storage.all("City")
    for city in cities.values():
        if state_id == getattr(city, "state_id"):
            city_list.append(city.to_dict())
    return jsonify(city_list), 200


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def retrieve_city(city_id):
    """retrieving the city id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/city/<city_id>", methods=['DELETE'], strict_slashes=False)
def deleting_city(city_id):
    """deleting a state"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", mehtods=['POST'], strict_slashes=False)
def creating_city(state_id):
    """creating a city"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if post_data.get("name") is None:
        abort(400, "Missing name")
    check_state = storage.get("state", state_id)
    if check_state is None:
        abort(404)
    post_data["state_id"] = state_id
    new_city = City(**post_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updating the state"""
    keys_ignored = ['id', 'created_at', 'updated_at']
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(404, "Not a JSON")
    for key, value in put_data.items():
        if key in keys_ignored:
            pass
        else:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
