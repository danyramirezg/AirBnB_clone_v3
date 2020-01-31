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
    reviews_list = []
    review_objs = storage.all('Review').values()
    for element in review_objs:
        reviews_list.append(element.to_dict())
    print(reviews_list)
    return jsonify(reviews_list)


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_list(place_id):
    """Retrieves a Review object."""
    reviews_list = []
    places_objs = storage.get('Place', place_id)
    if places_objs is None:
        abort(404)
    for places in places_objs.reviews:
        reviews_list.append(places.to_dict())

    return jsonify(reviews_list)
