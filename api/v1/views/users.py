#!/usr/bin/python3
"""New view for User object"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_list():
    """Retrieves the list of all User objects"""
    users_list = []
    users_objs = storage.all('User').values()
    for element in users_objs:
        users_list.append(element.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def users_list_id(user_id):
    """Retrieves a User object"""
    users_objs = storage.all('User').values()
    for element in users_objs:
        if element.id == user_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def user_remove(user_id):
    """Deletes a User object:"""
    user_to_delete = storage.get('User', user_id)
    if user_to_delete is None:
        abort(404)
    storage.delete(user_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
    """Creates User object"""
    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")
    if not user_data.get('email'):
        abort(400, "Missing email")
    if not user_data.get('password'):
        abort(400, "Missing password")
    new_user = User(**user_data)
    storage.new(new_user)
    new_user.save()
    return make_response(jsonify(new_user.to_dict())), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def user_update(user_id):
    """Updates a User object"""
    data_to_be_updated = request.get_json()
    if data_to_be_updated is None:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    user_to_update = storage.get('User', user_id)
    if user_to_update is None:
        abort(404)
    for key, value in data_to_be_updated.items():
        if key not in ignored_keys:
            setattr(user_to_update, key, value)
    user_to_update.save()
    return jsonify(user_to_update.to_dict()), 200
