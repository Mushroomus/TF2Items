from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from app.middleware import check_session_middleware

items_bp = Blueprint('items', __name__)

# MongoDB connection
client = MongoClient("mongodb+srv://test:test@cluster0.jjgvxkt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["tf"]

collection = db["items"]
collectionUser = db["users"]


@items_bp.route('/item', methods=['POST'])
@check_session_middleware
def create():
    data = request.json
    required_fields = ["name"]

    if data:
        # Check if all required fields are present
        if all(field in data for field in required_fields):
            result = collection.insert_one(data)
            return jsonify({"message": "Document created successfully", "id": str(result.inserted_id)}), 201
        else:
            missing_fields = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    else:
        return jsonify({"error": "No data provided"}), 400


@items_bp.route('/items', methods=['GET'], endpoint="get_items")
@check_session_middleware
def read_all():
    documents = list(collection.find())

    for doc in documents:
        doc["_id"] = str(doc["_id"])

    return jsonify(documents), 200


@items_bp.route('/item/<string:id>', methods=['PUT'], endpoint="put_item")
@check_session_middleware
def update(id):
    data = request.json
    if data:
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Document updated successfully"}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    else:
        return jsonify({"error": "No data provided"}), 400


@items_bp.route('/item/<string:id>', methods=['DELETE'], endpoint="delete_item")
@check_session_middleware
def delete(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Document deleted successfully"}), 200
    else:
        return jsonify({"error": "Document not found"}), 404


@items_bp.route('/item/favourites/<string:id>', methods=['GET'], endpoint="get_favourites_item")
@check_session_middleware
def get_item_favourites(id):
    try:
        # Perform aggregation
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            {"$unwind": "$favorites"},
            {"$lookup": {
                "from": "items",
                "localField": "favorites",
                "foreignField": "_id",
                "as": "itemDetails"
            }},
            {"$project": {
                "_id": 0,
                "name": {"$arrayElemAt": ["$itemDetails.name", 0]},
                "image": {"$arrayElemAt": ["$itemDetails.image", 0]}
            }}
        ]
        result = list(collectionUser.aggregate(pipeline))

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500