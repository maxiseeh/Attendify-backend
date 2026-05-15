# jwt_guard.py
# This file checks if a user is logged in before they can access protected routes.
# It uses JWT (JSON Web Token) to do that — basically a secure "ticket" the user gets after logging in.

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


# This is a decorator — you put it on top of a route to protect it.
# If the user doesn't have a valid token, they get a 401 error.
def jwt_required_guard(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Check if the request has a valid JWT token
            verify_jwt_in_request()
        except Exception as e:
            # Token is missing, expired, or invalid
            return jsonify({"message": "You need to log in first.", "error": str(e)}), 401

        # Token is fine, continue to the actual route
        return f(*args, **kwargs)

    return decorated_function


# A simple helper to get the ID of the currently logged-in user from the token
def get_current_user_id():
    return get_jwt_identity()