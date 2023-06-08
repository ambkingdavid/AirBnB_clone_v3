#!/usr/bin/python3

"""
a new view for State objects that handles all default RESTFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def retrieve_place(city_id):
    """
    Retrieves all places linked to a city
    """

    place_list = []
    city = storage.get(City, city_id)
    if city:
        for i in city.places:
            place_list.append(i.to_dict())
        return jsonify(place_list)
    abort(404)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_place_using_placeid(place_id):
    """
    REtrieves the place using the place id
    Raises a 404 error if the place_id isnt linked to a place
    """

    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place_using_placeid(place_id):
    """
    Deletes a placee using the place id
    Raises a 404 error If the place_id is not linked to any Place object
    Returns an empty dictionary with the status code 200
    """

    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """
    Posts a new place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    place_data = request.get_json()
    place_data['city_id'] = city_id
    place = Place()
    user = storage.get(User, place_data['user_id'])
    if not user:
        abort(404)
    for key, value in place_data.items():
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a place  using the place id
    Returns a 404 error if the place id is not linked to any place
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place = storage.get(Place, place_id)
    keys_ignore = ["id", "user_id", "city_id", "updated_at", "created_at"]
    if place:
        for key, value in request.get_json().items():
            if key not in keys_ignore:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        places route to handle http method for request to search places
    """
    all_places = [p for p in storage.all(Place).values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all(City).values()
        state_cities = set([city.id for city in all_cities
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get(City, c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_dict() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get(Amenity, a_id)])
        for p in all_places:
            p_amenities = None
            if STORAGE_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p.to_dict())
    else:
        places_amenities = [p.to_dict() for p in all_places]
    result = [
            {k: [v_elem.to_dict() if isinstance(v_elem, Amenity)
                 else v_elem for v_elem in v]
                if isinstance(v, list) else v
                for k, v in d.items()}
            for d in places_amenities
        ]

    return jsonify(result)
