import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from app.middleware import check_session_middleware

load_dotenv()
users_bp = Blueprint('users', __name__)

mongo_client_url = os.environ.get('MONGO_CLIENT_URL')
client = MongoClient(mongo_client_url)
db = client["tf"]
collection = db["users"]


@users_bp.route('/register', methods=['POST'], endpoint="register_user")
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


@users_bp.route('/login', methods=['POST'], endpoint="login_user")
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


@users_bp.route('/logout', methods=['GET'], endpoint="logout_user")
@check_session_middleware
def logout():
    session.pop('username', None)
    session.pop('admin', None)
    return redirect(url_for('files.login'))