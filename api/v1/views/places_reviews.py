#!/usr/bin/python3

"""
a new view for Review object that handles all default RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, abort, make_response, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def retrieve_review_uisng_placeid(place_id):
    """
    retrieves all review objects of a place
    raises a 404 error if the place_id isnt linked to any review
    """

    review_list = []
    place = storage.get(Place, place_id)
    if place:
        for reviewid in place.reviews:
            review_list.append(reviewid.to_dict())
        return jsonify(review_list)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_review(review_id):
    """
    Retrieves a review using the review id
    Raises a 404 error if the review_id isnt linked to any review
    """

    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    delets a review
    """

    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                    strict_slashes=False)
def post_review(place_id):
    """Posts a new review"""
    form = request.get_json()
    if not form:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if "user_id" not in form:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if "text" not in form:
        return make_response(jsonify({"error": "Missing text"}), 400)
    user = storage.get(User, form["user_id"])
    if not user:
        abort(404)
    form["place_id"] = place_id
    review = Review()
    for key, value in form.items():
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a review using the review_id
    """
    form = request.get_json()
    if not form:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    review = storage.get(Review, review_id)
    keys_ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    if review:
        for key, value in form.items():
            if key not in keys_ignore:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    abort(404)
