#!/usr/bin/python3
"""module for the city file"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users", methods=['Get'], strict_slashes=False)
def retrieving_users():
    """retrieving the list of the users"""
    users_list = []
    users = storage.all("User")
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """retrieving the user id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<users_id>", methods=['DELETE'], strict_slashes=False)
def deleting_user(user_id):
    """deleting a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", mehtods=['POST'], strict_slashes=False)
def creating_user():
    """creating users"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if post_data.get("email") is None:
        abort(400, "Missing email")
    if post_data.get("password") is None:
        abort(404, "Missing password")
    new_user = User(**post_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updating the user"""
    keys_ignored = ['id', 'created_at', 'updated_at', 'email']
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(404, "Not a JSON")
    for key, value in put_data.items():
        if key in keys_ignored:
            pass
        else:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
