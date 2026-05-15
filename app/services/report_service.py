from app.models.attendance import Attendance
from app.models.session import Session
from app.models.connection_log import ConnectionLog
from app.models.device import Device


class ReportService:

    @staticmethod
    def student_report(student_id):

        attendance_records = Attendance.query.filter_by(
            student_id=student_id
        ).all()

        total_sessions = len(attendance_records)

        present_sessions = 0
        absent_sessions = 0

        attendance_history = []

        for record in attendance_records:

            if record.status == "present":
                present_sessions += 1

            elif record.status == "absent":
                absent_sessions += 1

            attendance_history.append({
                "session_id": record.session_id,
                "status": record.status,
                "marked_at": str(record.marked_at)
            })

        attendance_percentage = 0

        if total_sessions > 0:
            attendance_percentage = round(
                (present_sessions / total_sessions) * 100,
                2
            )

        connection_logs = ConnectionLog.query.join(Device).filter(
            Device.user_id == student_id
        ).all()

        device_activity = []

        for log in connection_logs:

            device_activity.append({
                "device_id": log.device_id,
                "connected_at": str(log.connected_at),
                "disconnected_at": (
                    str(log.disconnected_at)
                    if log.disconnected_at else None
                ),
                "duration_minutes": log.duration_minutes,
                "status": log.status
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

        session = Session.query.get(session_id)

        if not session:
            return {
                "message": "Session not found"
            }, 404

        attendance_records = Attendance.query.filter_by(
            session_id=session_id
        ).all()

        students_present = 0
        students_absent = 0

        session_attendance = []

        for record in attendance_records:

            if record.status == "present":
                students_present += 1

            elif record.status == "absent":
                students_absent += 1

            session_attendance.append({
                "student_id": record.student_id,
                "status": record.status,
                "marked_at": str(record.marked_at)
            })

        return {
            "session_id": session.id,
            "course_name": session.course_name,
            "start_time": str(session.start_time),
            "end_time": str(session.end_time),
            "is_active": session.is_active,
            "total_students": len(attendance_records),
            "students_present": students_present,
            "students_absent": students_absent,
            "attendance_records": session_attendance
        }, 200

    @staticmethod
    def overall_statistics():

        total_attendance_records = Attendance.query.count()

        total_present = Attendance.query.filter_by(
            status="present"
        ).count()

        total_absent = Attendance.query.filter_by(
            status="absent"
        ).count()

        total_connections = ConnectionLog.query.count()

        return {
            "total_attendance_records": total_attendance_records,
            "total_present": total_present,
            "total_absent": total_absent,
            "total_connections": total_connections
        }, 200