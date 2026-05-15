"""
tests/test_models.py
Basic model and relationship testing
"""
from datetime import datetime
from app.models.user import User
from app.models.session import Session
from app.models.attendance import Attendance, AttendanceStatus
from app.models.device import Device


def test_user_model(db_session):
    user = User(fullname="Test User", email="test@test.com", password_hash="hash", role="student")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.fullname == "Test User"


def test_lecture_session(db_session, test_lecturer, test_wifi):
    session = Session(
        lecturer_id=test_lecturer.id,
        wifi_network_id=test_wifi.id,
        session_name="Database Systems - Lecture 4",
        start_time=datetime.utcnow(),
        is_active=True
    )
    db_session.add(session)
    db_session.commit()

    assert session.lecturer == test_lecturer
    assert len(test_lecturer.lecturer_sessions) >= 1


def test_attendance(db_session, test_student, test_lecturer, test_wifi):
    session = Session(
        lecturer_id=test_lecturer.id,
        wifi_network_id=test_wifi.id,
        session_name="Test Session",
        start_time=datetime.utcnow()
    )
    db_session.add(session)
    db_session.commit()

    attendance = Attendance(
        student_id=test_student.id,
        session_id=session.id,
        status=AttendanceStatus.PRESENT,
        check_in=datetime.utcnow()
    )
    db_session.add(attendance)
    db_session.commit()

    assert attendance.student == test_student
    assert attendance.status == AttendanceStatus.PRESENT