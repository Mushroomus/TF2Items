import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from app.middleware import check_session_middleware

load_dotenv()
favourites_bp = Blueprint('favourites', __name__)

# MongoDB connection
mongo_client_url = os.environ.get('MONGO_CLIENT_URL')
client = MongoClient(mongo_client_url)
db = client["tf"]

collection = db["items"]
collectionUser = db["users"]


@favourites_bp.route('/favourite', methods=['POST'], endpoint="post_favourite")
@check_session_middleware
def add_favourite():
    data = request.get_json()
    # Extract data from JSON payload
    user_id = data.get('userId')
    item_id = data.get('itemId')

    # Check if user exists in the database
    user = collectionUser.find_one({"_id": ObjectId(user_id)})
    if user:
        # Check if the item is already in the user's favorites
        if ObjectId(item_id) in user.get('favorites', []):
            return jsonify({"message": "Item already in favorites"}), 400

        # Update user's favorites in the database
        collectionUser.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"favorites": ObjectId(item_id)}}
        )
        return jsonify({"message": "Item added to favorites successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@favourites_bp.route('/favourite', methods=['DELETE'])
@check_session_middleware
def delete_favourite():
    data = request.get_json()
    # Extract data from JSON payload
    user_id = data.get('userId')
    item_id = data.get('itemId')

    # Check if user exists in the database
    user = collectionUser.find_one({"_id": ObjectId(user_id)})
    if user:
        # Check if the item is already in the user's favorites
        if not ObjectId(item_id) in user.get('favorites', []):
            return jsonify({"message": "Item already not in favorites"}), 400

        # Update user's favorites in the database
        collectionUser.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"favorites": ObjectId(item_id)}}
        )
        return jsonify({"message": "Item deleted from favorites successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@favourites_bp.route('/favourites/<string:id>', methods=['GET'], endpoint="get_favourite")
@check_session_middleware
def get_user_favourite(id):
    user = collectionUser.find_one({"_id": ObjectId(id)})
    if user:
        favorites = user.get('favorites', [])
        # Convert each ObjectId to string
        favorites_str = [str(ObjectId(favorite)) for favorite in favorites]
        return jsonify({"favorites": favorites_str}), 200
    else:
        return jsonify({"error": "User not found"}), 404
