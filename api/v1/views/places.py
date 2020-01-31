#!/usr/bin/python3
"""New view for Place objects"""
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def all_places():
    """Retrieves the list of all Place objects of a City"""
    places_list = []
    states_objs = storage.all('Place').values()
    for element in states_objs:
        places_list.append(element.to_dict())
    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_list(city_id):
    """Retrieves a Place object"""
    places_list = []
    cities_objs = storage.get('City', city_id)
    if cities_objs is None:
        abort(404)
    for places in cities_objs.places:
        places_list.append(places.to_dict())

    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_list_id(place_id):
    """Retrieves a Place object"""
    places_objs = storage.all('Place').values()
    for element in places_objs:
        if element.id == place_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def places_remove(place_id):
    """Deletes a Place object"""
    place_to_delete = storage.get('Place', place_id)
    if place_to_delete is None:
        abort(404)
    place_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def new_place(city_id):
    """Creates a Place"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    place_data = request.get_json()
    if place_data is None:
        abort(400, "Not a JSON")
    if not place_data.get('name'):
        abort(400, "Missing name")
    if not place_data.get('user_id'):
        abort(400, "Missing user_id")
    user_obj = storage.get('User', place_data.get('user_id'))
    if user_obj is None:
        abort(404)
    place_data['city_id'] = city_id
    place_data['user_id'] = place_data.get('user_id')
    new_city = Place(**place_data)
    storage.new(new_city)
    storage.save()
    storage.reload()
    return make_response(jsonify(new_city.to_dict())), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_update(place_id):
    """Updates a Place"""
    ignored_keys = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
    place_to_update = storage.get('Place', place_id)
    if place_to_update is None:
        abort(404)
    data_to_be_updated = request.get_json()
    if data_to_be_updated is None:
        abort(400, "Not a JSON")
    for key, value in data_to_be_updated.items():
        if key not in ignored_keys:
            setattr(place_to_update, key, value)
    place_to_update.save()
    storage.reload()
    return jsonify(place_to_update.to_dict()), 200
