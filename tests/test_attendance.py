"""
tests/test_attendance.py
"""
from datetime import datetime
from app.models.attendance import Attendance, AttendanceStatus
from app.models.session import Session


def test_attendance_creation(db_session, test_student, test_lecturer, test_wifi):
    # Create session first
    session = Session(
        lecturer_id=test_lecturer.id,
        wifi_network_id=test_wifi.id,
        session_name="Chemistry 101",
        start_time=datetime.utcnow(),
        is_active=True
    )
    db_session.add(session)
    db_session.commit()

    attendance = Attendance(
        student_id=test_student.id,
        session_id=session.id,
        check_in=datetime.utcnow(),
        status=AttendanceStatus.PRESENT
    )
    db_session.add(attendance)
    db_session.commit()
    db_session.refresh(attendance)

    assert attendance.student == test_student
    assert attendance.session == session
    assert attendance.status == AttendanceStatus.PRESENT