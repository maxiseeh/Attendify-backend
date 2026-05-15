from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.services.wifi_service import scan_wifi_devices


wifi_bp = Blueprint(
    "wifi",
    __name__,
    url_prefix="/api/wifi"
)


@wifi_bp.route("/scan", methods=["GET"])
@jwt_required()
def scan():

    result = scan_wifi_devices()

    return jsonify(result), 200