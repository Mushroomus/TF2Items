from flask import Flask
from flask_cors import CORS
from app.users.routes import users_bp
from app.files.routes import files_bp

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

app.register_blueprint(users_bp)
app.register_blueprint(files_bp)