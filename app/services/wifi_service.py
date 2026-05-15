from datetime import datetime

from app.extensions import db

from app.models.device import Device
from app.models.session import Session

from app.services.connection_service import (
    connect_device,
    disconnect_device
)

from app.services.attendance_service import AttendanceService


def scan_wifi_devices():

    detected_mac_addresses = [
        "AA:BB:CC:11:22:33",
        "FF:EE:DD:44:55:66"
    ]

    connected_devices = []

    active_session = Session.query.filter_by(
        is_active=True
    ).first()

    devices = Device.query.all()

    for device in devices:

        if device.mac_address in detected_mac_addresses:

            device.last_seen = datetime.utcnow()

            if not device.is_connected:

                connect_device(device)

                device.is_connected = True

                if active_session:

                    AttendanceService.mark_attendance({
                        "student_id": device.user_id,
                        "session_id": active_session.id,
                        "status": "present"
                    })

            connected_devices.append({
                "student_id": device.user_id,
                "device_name": device.device_name,
                "device_type": device.device_type,
                "mac_address": device.mac_address,
                "status": "connected",
                "last_seen": str(device.last_seen)
            })

        else:

            if device.is_connected:

                disconnect_device(device)

                device.is_connected = False

    db.session.commit()

    return {
        "message": "WiFi scan completed successfully",
        "total_connected_devices": len(connected_devices),
        "connected_devices": connected_devices
    }