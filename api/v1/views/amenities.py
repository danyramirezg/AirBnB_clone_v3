#!/usr/bin/python3
"""New view for Amenity objects"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_list():
    """Retrieves the list of all Amenity objects"""
    amenities_list = []
    amenities_objs = storage.all('Amenity').values()
    for element in amenities_objs:
        amenities_list.append(element.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenities_list_id(amenity_id):
    """Retrieves a Amenity object"""
    amenities_objs = storage.all('Amenity').values()
    for element in amenities_objs:
        if element.id == amenity_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_remove(amenity_id):
    """Deletes a Amenity object"""
    amenity_to_delete = storage.get('Amenity', amenity_id)
    if amenity_to_delete is None:
        abort(404)
    storage.delete(amenity_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def new_amenity():
    """Creates a new amenity"""
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")
    if not amenity_data.get('name'):
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenity_update(amenity_id):
    """Updates a Amenity object"""
    data_for_update = request.get_json()
    if data_for_update is None:
        abort(400, "Not a JSON")
    forbiden_keys = ['id', 'created_at', 'updated_at']
    amenity_to_update = storage.get('Amenity', amenity_id)
    if amenity_to_update is None:
        abort(404)
    for key, value in data_for_update.items():
        if key not in forbiden_keys:
            setattr(amenity_to_update, key, value)
    amenity_to_update.save()
    return jsonify(amenity_to_update.to_dict()), 200
