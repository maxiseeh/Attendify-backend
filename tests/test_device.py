"""
tests/test_device.py
"""
from app.models.device import Device


def test_device_creation(db_session):
    device = Device(
        mac_address="AA:BB:CC:DD:EE:FF",
        device_name="iPhone 14 Pro",
        device_type="phone",
        verified=True
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    assert device.id is not None
    assert device.is_auto_login_ready is True


def test_device_to_dict(db_session):
    device = Device(
        mac_address="11:22:33:44:55:66",
        device_name="Dell Laptop",
        verified=False
    )
    db_session.add(device)
    db_session.commit()

    data = device.to_dict()
    assert data["mac_address"] == "11:22:33:44:55:66"
    assert data["verified"] is False