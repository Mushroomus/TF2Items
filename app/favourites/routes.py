from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from pymongo import MongoClient

favourites_bp = Blueprint('favourites', __name__)

# MongoDB connection
client = MongoClient("mongodb+srv://test:test@cluster0.jjgvxkt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["tf"]

collection = db["items"]
collectionUser = db["users"]


@favourites_bp.route('/favourite', methods=['POST'])
def add_favourite():
    data = request.get_json()
    # Extract data from JSON payload
    user_id = data.get('userId')
    item_id = data.get('itemId')

    # Check if user exists in the database
    user = collectionUser.find_one({"_id": ObjectId(user_id)})
    if user:
        # Update user's favorites in the database
        collectionUser.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"favorites": ObjectId(item_id)}}
        )
        return jsonify({"message": "Item added to favorites successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@favourites_bp.route('/favourite', methods=['DELETE'])
def delete_favourite():
    data = request.get_json()
    # Extract data from JSON payload
    user_id = data.get('userId')
    item_id = data.get('itemId')

    # Check if user exists in the database
    user = collectionUser.find_one({"_id": ObjectId(user_id)})
    if user:
        # Update user's favorites in the database
        collectionUser.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"favorites": ObjectId(item_id)}}
        )
        return jsonify({"message": "Item added to favorites successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@favourites_bp.route('/favourites/<string:id>', methods=['GET'])
def get_user_favourite(id):
    user = collectionUser.find_one({"_id": ObjectId(id)})
    if user:
        favorites = user.get('favorites', [])
        # Convert each ObjectId to string
        favorites_str = [str(ObjectId(favorite)) for favorite in favorites]
        return jsonify({"favorites": favorites_str}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@favourites_bp.route('/favourite/<string:id>', methods=['DELETE'])
def delete(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Document deleted successfully"}), 200
    else:
        return jsonify({"error": "Document not found"}), 404