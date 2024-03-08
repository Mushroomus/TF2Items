from flask import Blueprint, render_template

files_bp = Blueprint('files', __name__)


@files_bp.route('/')
def index():
    return render_template('Login.html')

@files_bp.route('/ManageItems')
def manage_items():
    return render_template('ManageItems.html')


@files_bp.route('/BrowseItems')
def browse_items():
    return render_template('BrowseItems.html')


@files_bp.route('/FavouriteItems')
def favourite_items():
    return render_template('FavouriteItems.html')


@files_bp.route('/Login')
def login():
    return render_template('Login.html')


@files_bp.route('/Register')
def register():
    return render_template('Register.html')

