from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def jwt_required_guard(f):
    """Decorator — blocks the route if no valid JWT token is present."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"message": "You need to log in first.", "error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function


def get_current_user_id():
    """Returns the ID of the currently logged-in user from their token."""
    return get_jwt_identity()
