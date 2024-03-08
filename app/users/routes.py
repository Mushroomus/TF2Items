from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

users_bp = Blueprint('users', __name__)

client = MongoClient("mongodb+srv://test:test@cluster0.jjgvxkt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["tf"]
collection = db["users"]


@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if data:
        username = data.get('username')
        password = data.get('password')
        admin = data.get('admin')
        if username and password:
            if collection.find_one({"username": username}):
                return jsonify({"error": "Username already exists"}), 400
            else:
                hashed_password = generate_password_hash(password)
                collection.insert_one({"username": username, "password": hashed_password, "admin": admin})
                return jsonify({"message": "Registration successful"}), 201
        else:
            return jsonify({"error": "Username or password missing"}), 400
    else:
        return jsonify({"error": "No data provided"}), 400


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if data:
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = collection.find_one({"username": username})
            if user and check_password_hash(user["password"], password):
                session['username'] = username
                session['admin'] = user["admin"]
                return jsonify({"message": "Login successful", "id": str(user["_id"]), "admin": user["admin"]}), 200
            else:
                return jsonify({"error": "Invalid username or password"}), 401
        else:
            return jsonify({"error": "Username or password missing"}), 400
    else:
        return jsonify({"error": "No data provided"}), 400


@users_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('admin', None)
    return redirect(url_for('files.login'))