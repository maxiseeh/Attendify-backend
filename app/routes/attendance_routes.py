# here the file deals with attendance record
# Marks students present
# Marks students absent
# Retrieves attendance history
# Calculates attendance percentage

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.attendance_service import AttendanceService


attendance_bp = Blueprint(
    "attendance",
    __name__,
    url_prefix="/api/attendance"
)


@attendance_bp.route("/mark", methods=["POST"])
@jwt_required()
def mark_attendance():

    data = request.get_json()

    result, status = AttendanceService.mark_attendance(data)

    return jsonify(result), status


@attendance_bp.route("/session/<int:session_id>", methods=["GET"])
@jwt_required()
def get_session_attendance(session_id):

    result, status = AttendanceService.get_by_session(session_id)

    return jsonify(result), status


@attendance_bp.route("/student/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student_attendance(student_id):

    result, status = AttendanceService.get_by_student(student_id)

    return jsonify(result), status


@attendance_bp.route("/record/<int:record_id>", methods=["GET"])
@jwt_required()
def get_record(record_id):

    result, status = AttendanceService.get_record(record_id)

    return jsonify(result), status


@attendance_bp.route("/percentage/<int:student_id>", methods=["GET"])
@jwt_required()
def get_percentage(student_id):

    result, status = AttendanceService.calculate_percentage(student_id)

    return jsonify(result), status