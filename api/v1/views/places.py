#!/usr/bin/python3
"""module for the city file"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['Get'], strict_slashes=False)
def retrieving_places(city_id):
    """retrieving the list of the places"""
    places_list = []
    check_city = storage.get("City", city_id)
    if check_city is None:
        abort(404)
    places = storage.all("Place")
    for place in places.values():
        if city_id == getattr(place, "city_id"):
            places_list.append(place.to_dict())
    return jsonify(places_list), 200


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def retrieve_place(place_id):
    """retrieving the place id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/place_id>", methods=['DELETE'], strict_slashes=False)
def deleting_places(place_id):
    """deleting a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/cities", mehtods=['POST'], strict_slashes=False)
def creating_place(city_id):
    """creating a city"""
    post_data = request.get_json()
    check_city = storage.get("City", city_id)
    if check_city is None:
        abort(404)
    if post_data is None:
        abort(400, 'Not a JSON')
    if post_data.get('user_id') is None:
        abort(400, 'Missing user_id')
    user_id = post_data['user_id']
    check_user = storage.get("User", user_id)
    if check_user is None:
        abort(404)
    if post_data.get('name') is None:
        abort(400, 'Missing name')
    post_data['city_id'] = city_id
    new_place = Place(**post_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updating the place"""
    keys_ignored = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(404, "Not a JSON")
    for key, value in put_data.items():
        if key in keys_ignored:
            pass
        else:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
