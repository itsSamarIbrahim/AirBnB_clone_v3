#!/usr/bin/python3
"""
Module for displaying and searching through places for rent
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user_id = data['user_id']
    if not storage.get(User, user_id):
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for places based on JSON parameters"""
    request_data = request.get_json()

    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400

    states = request_data.get("states")
    cities = request_data.get("cities")
    amenities = request_data.get("amenities")

    if not states and not cities and not amenities:
        places = storage.all("Place").values()
        return jsonify([place.to_dict() for place in places])

    place_ids = set()

    if states:
        for state_id in states:
            state = storage.get("State", state_id)
            if state:
                for city in state.cities:
                    place_ids.update({place.id for place in city.places})

    if cities:
        for city_id in cities:
            city = storage.get("City", city_id)
            if city:
                place_ids.update({place.id for place in city.places})

    if amenities:
        for amenity_id in amenities:
            amenity = storage.get("Amenity", amenity_id)
            if amenity:
                if not place_ids:
                    place_ids.update({place.id for place in amenity.places})
                else:
                    place_ids.intersection_update(
                        {place.id for place in amenity.places})

    places = [storage.get("Place", place_id) for place_id in place_ids]

    return jsonify([place.to_dict() for place in places])
