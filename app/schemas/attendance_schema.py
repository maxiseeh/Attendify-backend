# attendance_schema.py
# This file validates attendance data.
# Attendance records track when and how students checked in to a class session.

from marshmallow import Schema, fields, validate
from datetime import datetime


class AttendanceMarkSchema(Schema):
    """
    Schema for marking a student as present.
    Used when a student checks in via QR code or device MAC address.
    """
    
    # ID of the student marking attendance
    student_id = fields.Int(required=True)
    
    # ID of the session (class/lecture) they're attending
    session_id = fields.Int(required=True)
    
    # How did they check in? "qr_code", "device_mac", or "manual"
    check_in_method = fields.Str(
        required=True,
        validate=validate.OneOf(["qr_code", "device_mac", "manual"]),
        error_messages={"required": "Check-in method is required"}
    )
    
    # The device's MAC address (if they checked in via WiFi)
    # Optional because they might check in via QR code instead
    device_mac = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(min=17, max=17)
    )
    
    # Timestamp when they checked in
    # If not provided, server will use current time
    check_in_time = fields.DateTime(
        required=False,
        allow_none=True
    )


class AttendanceRecordSchema(Schema):
    """
    Schema for displaying attendance records.
    Shows the complete attendance information.
    """
    
    # Record ID - unique identifier for this attendance record
    id = fields.Int(dump_only=True)
    
    # Which student checked in
    student_id = fields.Int()
    
    # Which class session they attended
    session_id = fields.Int()
    
    # Method used to check in
    check_in_method = fields.Str()
    
    # Device MAC if they checked in via WiFi
    device_mac = fields.Str()
    
    # Exact time they checked in
    check_in_time = fields.DateTime()
    
    # When this record was created in database
    created_at = fields.DateTime(dump_only=True)


class StudentAttendanceSchema(Schema):
    """
    Schema for getting all attendance records for one student.
    Useful for reports and tracking student participation.
    """
    
    # Student's ID
    student_id = fields.Int()
    
    # Student's name
    student_name = fields.Str()
    
    # Total classes attended
    classes_attended = fields.Int()
    
    # Total classes the student should have attended
    total_classes = fields.Int()
    
    # Attendance percentage (like 85%)
    attendance_percentage = fields.Float()
    
    # List of all attendance records
    records = fields.List(fields.Nested(AttendanceRecordSchema))


class SessionAttendanceSchema(Schema):
    """
    Schema for getting all attendance records for one session/class.
    Shows who attended a particular class.
    """
    
    # Session/Class ID
    session_id = fields.Int()
    
    # Session date and time
    session_date = fields.DateTime()
    
    # Total students who attended
    students_present = fields.Int()
    
    # Total students who should have attended
    total_students = fields.Int()
    
    # Attendance rate for this class (like 92%)
    attendance_rate = fields.Float()
    
    # List of all who checked in
    attendance_records = fields.List(fields.Nested(AttendanceRecordSchema))


class AttendanceSummarySchema(Schema):
    """
    Schema for overall attendance summary.
    Shows big picture statistics.
    """
    
    # Total attendance records in the system
    total_records = fields.Int()
    
    # Most common check-in method
    most_used_method = fields.Str()
    
    # Average attendance rate across all students
    average_attendance_rate = fields.Float()
    
    # Top date (the day with most check-ins)
    busiest_date = fields.DateTime()
    
    # Report generation timestamp
    generated_at = fields.DateTime()
