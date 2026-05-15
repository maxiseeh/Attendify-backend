from marshmallow import ValidationError
from datetime import datetime

from app.schemas.attendance_schema import AttendanceMarkSchema, AttendanceRecordSchema
from app.utils.duration_calculator import get_current_utc_time


class AttendanceService:

    @staticmethod
    def mark_attendance(data):
        try:
            schema = AttendanceMarkSchema()
            validated_data = schema.load(data)

            check_in_time = validated_data.get('check_in_time') or get_current_utc_time()

            

            return {
                "message": "Attendance marked successfully",
                "check_in_time": check_in_time.isoformat(),
                "method": validated_data['check_in_method']
            }, 201
        
        except ValidationError as e:
            return {"errors": e.messages}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_session(session_id):
        try:
            

            return {
                "message": "Session attendance retrieved",
                "session_id": session_id
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_student(student_id):
        try:
            

            return {
                "message": "Student attendance retrieved",
                "student_id": student_id
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_record(record_id):
        try:
           

            return {"message": "Record retrieved"}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def calculate_percentage(student_id):
        try:
            

            return {
                "message": "Percentage calculated",
                "student_id": student_id
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_summary():
        try:
            

            return {
                "message": "Summary generated",
                "generated_at": datetime.utcnow().isoformat()
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500
