import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from app.users.routes import users_bp
from app.items.routes import items_bp
from app.files.routes import files_bp
from app.favourites.routes import favourites_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
CORS(app)

app.register_blueprint(users_bp)
app.register_blueprint(files_bp)
app.register_blueprint(items_bp)
app.register_blueprint(favourites_bp)