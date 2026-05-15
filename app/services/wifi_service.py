# wifi_service.py
# This file handles scanning the WiFi network to detect which devices are connected.
# When a device is found, it logs the connection and marks attendance automatically.

from datetime import datetime

from app.extensions import db
from app.models.device import Device
from app.models.session import Session
from app.services.connection_service import ConnectionService


def scan_wifi_devices():
    """
    Scan the WiFi network and check which registered devices are connected.
    This is a simulated scan — in production this would talk to the router.
    """

    # These are the MAC addresses we "detected" on the WiFi network
    # In a real system, this list would come from the router or network scanner
    detected_macs = [
        "AA:BB:CC:11:22:33",
        "FF:EE:DD:44:55:66"
    ]

    connected_devices = []

    # Find the currently active lecture session (if any)
    active_session = Session.query.filter_by(is_active=True).first()

    # Get all registered devices from the database
    all_devices = Device.query.all()

    for device in all_devices:

        # Check if this device is currently on the WiFi network
        if device.mac_address in detected_macs:

            # Update the last time we saw this device
            device.last_seen = datetime.utcnow()

            # Log the connection event
            ConnectionService.log_connection(device.id)

            # If there's an active session, try to mark attendance
            # (Attendance marking needs student info linked to device — future feature)

            connected_devices.append({
                "device_id": device.id,
                "device_name": device.device_name,
                "mac_address": device.mac_address,
                "status": "connected",
                "last_seen": str(device.last_seen)
            })

    # Save all the changes (last_seen updates) to the database
    db.session.commit()

    return {
        "message": "WiFi scan completed successfully",
        "total_connected": len(connected_devices),
        "connected_devices": connected_devices,
        "active_session_id": active_session.id if active_session else None
    }