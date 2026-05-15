# These are the API endpoints for logging in, registering, and managing user accounts.
# URL prefix: /api/auth

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.auth_service import AuthService


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user (student, lecturer, or admin)."""

    data = request.get_json()
    result, status = AuthService.register(data)
    return jsonify(result), status


@auth_bp.route("/login", methods=["POST"])
def login():
    """Log in with email and password. Returns a JWT token."""

    data = request.get_json()
    result, status = AuthService.login(data)
    return jsonify(result), status


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Log out the currently logged-in user."""

    # Get the ID of the currently logged-in user from their token
    user_id = get_jwt_identity()
    result, status = AuthService.logout(user_id)
    return jsonify(result), status


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """Get the profile of the currently logged-in user."""

    # Get the ID of the currently logged-in user from their token
    user_id = get_jwt_identity()
    result, status = AuthService.profile(user_id)
    return jsonify(result), status