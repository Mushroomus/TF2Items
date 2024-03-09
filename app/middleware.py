from flask import jsonify, session


def check_session_middleware(func):
    def wrapper(*args, **kwargs):
        # Check if 'username' is in the session
        if 'username' in session:
            # Continue to the requested route function
            return func(*args, **kwargs)
        else:
            # Return an error response
            return jsonify({"error": "Unauthorized access"}), 401
    return wrapper

