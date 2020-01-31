#!/usr/bin/python3
"""States view module.."""
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def all_reviews():
    """Retrieves the list of all Review objects"""
    places_review_list = []
    review_objs = storage.all('Review').values()
    for element in review_objs:
        places_review_list.append(element.to_dict())
    print(places_review_list)
    return jsonify(places_review_list)


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def places_review_list(place_id):
    """Retrieves a Review object."""
    places_review_list = []
    places_review_objs = storage.get('Place', place_id)
    if places_review_objs is None:
        abort(404)
    for places in places_review_objs.reviews:
        places_review_list.append(places.to_dict())

    return jsonify(places_review_list)

@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def reviews_remove(review_id):
    """Deletes a Review object"""
    places_review_to_delete = storage.get('Review', review_id)
    if places_review_to_delete is None:
        abort(404)
    places_review_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def new_places_review(place_id):
    """Creates a new state"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    places_reviews_data = request.get_json()
    if places_reviews_data is None:
        abort(400, "Not a JSON")
    if not places_reviews_data.get('user_id'):
        abort(400, "Missing user_id")
    if not places_reviews_data.get('text'):
        abort(400, "Missing text")
    user_obj = storage.get('User', places_reviews_data.get('user_id'))
    if user_obj is None:
        abort(404)

    places_reviews_data['place_id'] = place_id
    new_places_review = Review(**places_reviews_data)
    storage.new(new_places_review)
    new_places_review.save()
    return make_response(jsonify(new_places_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_update(review_id):
    """Updates a Review object"""
    ignored_keys = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    place_review_to_update = storage.get('Review', review_id)
    if place_review_to_update is None:
        abort(404)
    data_for_update = request.get_json()
    if data_for_update is None:
        abort(400, "Not a JSON")
    for key, value in data_for_update.items():
        if key not in ignored_keys:
            setattr(place_review_to_update, key, value)
    place_review_to_update.save()
    storage.reload()
    return jsonify(place_review_to_update.to_dict()), 200
