from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.session_service import SessionService


session_bp = Blueprint(
    "sessions",
    __name__,
    url_prefix="/api/sessions"
)


@session_bp.route("/", methods=["GET"])
@jwt_required()
def list_sessions():

    result, status = SessionService.list_sessions()

    return jsonify(result), status


@session_bp.route("/", methods=["POST"])
@jwt_required()
def create_session():

    data = request.get_json()

    result, status = SessionService.create_session(data)

    return jsonify(result), status


@session_bp.route("/<int:session_id>", methods=["PUT"])
@jwt_required()
def update_session(session_id):

    data = request.get_json()

    result, status = SessionService.update_session(session_id, data)

    return jsonify(result), status


@session_bp.route("/<int:session_id>", methods=["DELETE"])
@jwt_required()
def delete_session(session_id):

    result, status = SessionService.close_session(session_id)

    return jsonify(result), status