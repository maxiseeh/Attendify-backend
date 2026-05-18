from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(required_role):
    """Decorator — blocks the route if the user's role doesn't match."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role", None)

            if user_role != required_role:
                return jsonify({
                    "message": f"Access denied. You need to be a '{required_role}' to do this."
                }), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
