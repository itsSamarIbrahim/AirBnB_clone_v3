#!/usr/bin/python3
"""
Module to allow examining the link between places and amenities
"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """
    Retrieve all Amenity objects of a Place
    """
    # Retrieve the Place object from storage
    place = storage.get("Place", place_id)
    if not place:
         abort(404)

    # Retrieve and return all Amenity objects of the Place
    amenities = place.amenities
    return jsonify([amenity.to_dict() for amenity in amenities])

    # For demonstration purposes, return a sample response
    return jsonify({"message": "GET place amenities"})


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Delete an Amenity object from a Place
    """
    # Retrieve the Place object from storage
    place = storage.get("Place", place_id)
    if not place:
         abort(404)

    # Retrieve the Amenity object from storage
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
         abort(404)

    # Check if the Amenity is linked to the Place
    if amenity not in place.amenities:
         abort(404)

    # Delete the Amenity from the Place
    place.amenities.remove(amenity)
    storage.save()

    # Return an empty dictionary with status code 200
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """
    Link an Amenity object to a Place
    """
    # Retrieve the Place object from storage
    place = storage.get("Place", place_id)
    if not place:
         abort(404)

    # Retrieve the Amenity object from storage
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
         abort(404)

    # Check if the Amenity is already linked to the Place
    if amenity in place.amenities:
         return jsonify(amenity.to_dict()), 200

    # Link the Amenity to the Place
    place.amenities.append(amenity)
    storage.save()

    # Return the Amenity with status code 201
    return jsonify({"message": "Link Amenity to Place"}), 201
