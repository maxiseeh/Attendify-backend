# report_service.py
# This file generates attendance reports.
# It can show reports for a single student, a single session, or overall stats.

from app.models.attendance import Attendance
from app.models.session import Session
from app.models.connection_log import ConnectionLog


class ReportService:

    @staticmethod
    def student_report(student_id):
        """
        Get an attendance report for one student.
        Shows how many classes they attended and their attendance percentage.
        """

        # Get all attendance records for this student
        attendance_records = Attendance.query.filter_by(student_id=student_id).all()

        total_sessions = len(attendance_records)
        present_sessions = 0
        absent_sessions = 0
        attendance_history = []

        for record in attendance_records:

            # Count present vs absent
            if record.status.value == "present":
                present_sessions += 1
            elif record.status.value == "absent":
                absent_sessions += 1

            attendance_history.append({
                "session_id": record.session_id,
                "status": record.status.value,
                # check_in is the correct field name (not marked_at)
                "check_in": str(record.check_in) if record.check_in else None
            })

        # Calculate attendance percentage
        attendance_percentage = 0
        if total_sessions > 0:
            attendance_percentage = round(
                (present_sessions / total_sessions) * 100, 2
            )

        # Get connection logs linked to this student's sessions
        connection_logs = ConnectionLog.query.join(
            Session, ConnectionLog.session_id == Session.id
        ).filter(
            Session.lecturer_id == student_id  # placeholder join until user-session link is added
        ).all()

        device_activity = []
        for log in connection_logs:
            device_activity.append({
                "device_id": log.device_id,
                "connected_at": str(log.connected_at),
                "disconnected_at": str(log.disconnected_at) if log.disconnected_at else None,
                # duration_seconds is the correct field (not duration_minutes)
                "duration_seconds": log.duration_seconds,
                "still_connected": log.is_connected
            })

        return {
            "student_id": student_id,
            "attendance_percentage": attendance_percentage,
            "total_sessions": total_sessions,
            "present_sessions": present_sessions,
            "absent_sessions": absent_sessions,
            "attendance_history": attendance_history,
            "device_activity": device_activity
        }, 200

    @staticmethod
    def session_report(session_id):
        """
        Get an attendance report for one session/class.
        Shows who attended and who was absent.
        """

        # Find the session
        session = Session.query.get(session_id)
        if not session:
            return {"error": "Session not found"}, 404

        # Get all attendance records for this session
        attendance_records = Attendance.query.filter_by(session_id=session_id).all()

        students_present = 0
        students_absent = 0
        session_attendance = []

        for record in attendance_records:

            if record.status.value == "present":
                students_present += 1
            elif record.status.value == "absent":
                students_absent += 1

            session_attendance.append({
                "student_id": record.student_id,
                "status": record.status.value,
                # check_in is the correct field name (not marked_at)
                "check_in": str(record.check_in) if record.check_in else None
            })

        return {
            "session_id": session.id,
            # session_name is the correct field (not course_name)
            "session_name": session.session_name,
            "start_time": str(session.start_time),
            "end_time": str(session.end_time) if session.end_time else None,
            "is_active": session.is_active,
            "total_students": len(attendance_records),
            "students_present": students_present,
            "students_absent": students_absent,
            "attendance_records": session_attendance
        }, 200

    @staticmethod
    def overall_statistics():
        """
        Get overall stats for the whole system.
        Shows totals for attendance and connections.
        """

        total_records = Attendance.query.count()
        total_present = Attendance.query.filter(
            Attendance.status.has(value="present")
        ).count()
        total_connections = ConnectionLog.query.count()

        return {
            "total_attendance_records": total_records,
            "total_connections": total_connections
        }, 200