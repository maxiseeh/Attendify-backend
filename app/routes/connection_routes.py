# tracks the wifi conection activities 
# the file tracks device connections
# device disconnections
# conn duration 
# active devices


from flask import Blueprint, jsonify

from app.models.connection_log import ConnectionLog


connection_bp = Blueprint(
    "connection",
    __name__,
    url_prefix="/api/connections"
)


@connection_bp.route("/logs", methods=["GET"])
def get_logs():

    logs = ConnectionLog.query.all()

    result = []

    for log in logs:

        result.append({
            "id": log.id,
            "device_id": log.device_id,
            "connected_at": str(log.connected_at),
            "disconnected_at": str(log.disconnected_at) if log.disconnected_at else None,
            "duration_minutes": log.duration_minutes,
            "status": log.status
        })

    return jsonify(result), 200


@connection_bp.route("/active", methods=["GET"])
def active_connections():

    logs = ConnectionLog.query.filter_by(status="connected").all()

    return jsonify([
        {
            "device_id": log.device_id,
            "connected_at": str(log.connected_at)
        }
        for log in logs
    ]), 200