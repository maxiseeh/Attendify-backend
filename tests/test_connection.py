"""
tests/test_connection.py
"""
from datetime import datetime
from app.models.connection_log import ConnectionLog
from app.models.session import Session


def test_connection_log_creation(db_session, test_lecturer, test_wifi):
    session = Session(
        lecturer_id=test_lecturer.id,
        wifi_network_id=test_wifi.id,
        session_name="Test Lecture",
        start_time=datetime.utcnow()
    )
    db_session.add(session)
    db_session.commit()

    log = ConnectionLog(
        session_id=session.id,
        device_id=None,
        connected_at=datetime.utcnow(),
        ip_address="192.168.1.45"
    )
    db_session.add(log)
    db_session.commit()

    assert log.session == session
    assert log.is_connected is True