from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.device_service import DeviceService


device_bp = Blueprint(
    "device",
    __name__,
    url_prefix="/api/devices"
)


@device_bp.route("/register", methods=["POST"])
@jwt_required()
def register_device():

    data = request.get_json()

    result, status = DeviceService.register_device(data)

    return jsonify(result), status


@device_bp.route("/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_devices(user_id):

    result, status = DeviceService.get_user_devices(user_id)

    return jsonify(result), status