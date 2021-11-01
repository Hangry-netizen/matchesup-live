from flask import Blueprint, jsonify, request
from models.report import Report
from models.gsc import Gsc
from helpers import sendgrid

reports_api_blueprint = Blueprint('reports_api',
                             __name__)

@reports_api_blueprint.route('/', methods=['GET'])
def index():
    reports = Report.select()
    response = []
    
    for report in reports:
        reported_by = report.reported_by
        report_target = report.report_target
        data = {
            "reported_by_name": reported_by.name,
            "reported_by_email": reported_by.email,
            "report_target_name": report_target.name,
            "report_target_email": report_target.email,
            "reason": report.reason,
            "archived": report.archived,
            "admin_remarks": report.admin_remarks
        }
        response.append(data)
        
    return jsonify(response)


@reports_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json
    
    reported_by = data.get("reported_by")
    report_target = data.get("report_target")
    reason = data.get("reason")
    
    if reported_by and report_target and reason:
        report = Report(
            reported_by = reported_by,
            report_target = report_target,
            reason = reason
        )
        
        if report.save():
            report_target = report.report_target
            return jsonify({
                "message": f"Successfully reported {report_target.name}",
                "status": "success"
            })
        
        else:
            return jsonify({
                "message": "Report was unsuccessful",
                "status": "failed"
            })
    else:
        return jsonify({
            "message": "At least one field must be filled",
            "status": "failed"
        })