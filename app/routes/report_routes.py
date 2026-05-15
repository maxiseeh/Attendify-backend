from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.services.report_service import ReportService


report_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/api/reports"
)


@report_bp.route("/student/<int:student_id>", methods=["GET"])
@jwt_required()
def student_report(student_id):

    result, status = ReportService.student_report(student_id)

    return jsonify(result), status


@report_bp.route("/session/<int:session_id>", methods=["GET"])
@jwt_required()
def session_report(session_id):

    result, status = ReportService.session_report(session_id)

    return jsonify(result), status


@report_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():

    result, status = ReportService.overall_statistics()

    return jsonify(result), status