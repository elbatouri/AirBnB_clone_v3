#!/usr/bin/python3
"""
View for City objects that handles default API actions.
"""

from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False
)
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects for a specific state.
    """
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route(
    '/cities/<city_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_city(city_id):
    """
    Retrieves a specific City object based on the given city_id.
    """
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_city(city_id):
    """
    Deletes a specific City object based on the given city_id.
    """
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    city.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
)
def create_city(state_id):
    """
    Creates a new City object for the specified state.
    """
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    new_city_data = request.get_json()

    if not new_city_data or "name" not in new_city_data:
        abort(400, "Invalid or missing JSON data")

    new_city = City(**new_city_data)
    new_city.state_id = state_id

    storage.new(new_city)
    storage.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_city(city_id):
    """
    Updates a specific City object based on the given city_id.
    """
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    request_data = request.get_json()

    if not request_data:
        abort(400, "Invalid or missing JSON data")

    for key, value in request_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
