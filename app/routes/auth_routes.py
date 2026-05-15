from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.auth_service import AuthService


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    result, status = AuthService.register(data)

    return jsonify(result), status


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    result, status = AuthService.login(data)

    return jsonify(result), status


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    result, status = AuthService.logout()

    return jsonify(result), status


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    result, status = AuthService.profile()

    return jsonify(result), status