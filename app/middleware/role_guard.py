# role_guard.py
# This file checks if the logged-in user has the right role to access a route.
# For example, only an "admin" should be able to create sessions.
# It works together with jwt_guard.py — jwt_guard checks login, role_guard checks permission.

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


# This decorator takes a role name and checks if the current user has that role.
# Usage example on a route:
#   @jwt_required_guard
#   @role_required("admin")
#   def some_admin_route():
#       ...
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the extra info stored inside the JWT token (we store role there during login)
            claims = get_jwt()

            # Read the user's role from the token claims
            user_role = claims.get("role", None)

            # If the role doesn't match, deny access
            if user_role != required_role:
                return jsonify({
                    "message": f"Access denied. You need to be a '{required_role}' to do this."
                }), 403

            # Role is correct, continue to the route
            return f(*args, **kwargs)

        return decorated_function
    return decorator