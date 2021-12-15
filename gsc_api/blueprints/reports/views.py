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
            "id": report.id,
            "reported_by_name": reported_by.name,
            "reported_by_email": reported_by.email,
            "report_target_name": report_target.name,
            "report_target_email": report_target.email,
            "reason": report.reason,
            "recommended_action": report.recommended_action,
            "resolved": report.resolved,
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
    recommended_action = data.get("recommended_action")
    
    if reported_by and report_target and reason:
        report = Report(
            reported_by = reported_by,
            report_target = report_target,
            reason = reason,
            recommended_action = recommended_action,
        )
        
        if report.save():
            reported_by = report.reported_by
            report_target = report.report_target

            admin_email = ["matchesup@gmail.com", "Jengoverseas@gmail.com"]
            report_admin_notification_template_id = "d-687dec242050416cac93277d63f82291"
            data = {
                "report_target_name": report_target.name,
                "reported_by_name": reported_by.name,
                "reason": reason
            }
                    
            send_email_to_admin = sendgrid(to_email=admin_email, dynamic_template_data=data, template_id=report_admin_notification_template_id)

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

@reports_api_blueprint.route('/delete/<id>', methods=['POST'])
def delete(id):
    report = Report.get_or_none(Report.id == id)

    if report:
        if report.delete_instance():
            return jsonify({
                "message": "Successfully deleted report",
                "status": "success"
            })
        else:
            return jsonify({
                "message": "Failed to delete report",
                "status": "failed"
            })
    else:
        return jsonify({
            "message": "Report can't be found",
            "status": "failed"
        })

@reports_api_blueprint.route('/resolve/<id>', methods=['POST'])
def resolve(id):
    report = Report.get_or_none(Report.id == id)

    if report:
        report.resolved = True

        if report.save(only=[Report.resolved]):
            return jsonify({
                "message": "Successfully marked report as resolved",
                "status": "success"
            })
        else:
            return jsonify({
                "message": "Failed to mark report as resolved",
                "status": "failed"
            })
    else:
        return jsonify({
            "message": "Report cannot be found",
            "status": "failed"
        })

@reports_api_blueprint.route('/update-remarks/<id>', methods=['POST'])
def update_remarks(id):
    report = Report.get_or_none(Report.id == id)

    data = request.json
    admin_remarks = data.get("admin_remarks")

    if (admin_remarks != ""):
        report.admin_remarks = admin_remarks

        if report.save(only=[Report.admin_remarks]):
            return jsonify({
                "message": "Successfully updated admin remarks",
                "status": "success"
            })

        else:
            return jsonify({
                "message": "Failed to update admin remarks",
                "status": "failed"
            })
    else:
        return jsonify({
            "message": "Admin remarks field is required",
            "status": "failed"
        })

