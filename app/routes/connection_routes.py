# These are the API endpoints for tracking device connections to the WiFi network.
# This tracks when devices connect and disconnect during a session.
# URL prefix: /api/connections

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.models.connection_log import ConnectionLog


connection_bp = Blueprint("connection", __name__, url_prefix="/api/connections")


@connection_bp.route("/logs", methods=["GET"])
@jwt_required()
def get_logs():
    """Get all connection logs (who connected and when)."""

    logs = ConnectionLog.query.all()

    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "device_id": log.device_id,
            "session_id": log.session_id,
            "connected_at": str(log.connected_at),
            # disconnected_at is None if device is still connected
            "disconnected_at": str(log.disconnected_at) if log.disconnected_at else None,
            # duration_seconds is the correct field from our ConnectionLog model
            "duration_seconds": log.duration_seconds,
            "is_connected": log.is_connected
        })

    return jsonify(result), 200


@connection_bp.route("/active", methods=["GET"])
@jwt_required()
def active_connections():
    """Get all devices that are currently connected (no disconnect time yet)."""

    # A device is still connected if disconnected_at is None
    logs = ConnectionLog.query.filter(ConnectionLog.disconnected_at == None).all()

    return jsonify([
        {
            "device_id": log.device_id,
            "session_id": log.session_id,
            "connected_at": str(log.connected_at)
        }
        for log in logs
    ]), 200