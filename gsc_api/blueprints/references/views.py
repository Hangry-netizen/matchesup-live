from flask import Blueprint, jsonify, request
from models.reference import Reference
from models.gsc import Gsc
from helpers import sendgrid

references_api_blueprint = Blueprint('references_api',
                             __name__)

@references_api_blueprint.route('/', methods=['GET'])
def index():
    references = Reference.select()

    return jsonify([{
        "ref_id": reference.id,
        "ref_name": reference.ref_name,
        "ref_email": reference.ref_email,
        "reasons_gscf_makes_a_good_partner": reference.reasons_gscf_makes_a_good_partner,
        "good_match_for_gscf": reference.good_match_for_gscf,
        "is_approved": reference.is_approved
    } for reference in references])

@references_api_blueprint.route('/gsc/<uuid>', methods=['GET'])
def get_reference(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)
    references = gsc.references

    return jsonify([{
        "ref_id": reference.id,
        "ref_name": reference.ref_name,
        "ref_email": reference.ref_email,
        "reasons_gscf_makes_a_good_partner": reference.reasons_gscf_makes_a_good_partner,
        "good_match_for_gscf": reference.good_match_for_gscf,
        "is_approved": reference.is_approved
    } for reference in references])
    
@references_api_blueprint.route('/send-reference-email/<ref_id>', methods=['POST'])
def send_reference(ref_id):
    reference = Reference.get_or_none(Reference.id == ref_id)

    if reference:
        gsc = reference.gsc
        template_id = "d-6af1d902e5544dc68eeab4fe99809219"
        data = {
                "gscf_name": gsc.name,
                "ref_name": reference.ref_name,
                "ref_url": f"https://www.matchesup.com/good-single-christian-friend/{gsc.uuid}/{reference.id}/reference/{reference.ref_name}"
            }
    
        send_reference_email = sendgrid(to_email=reference.ref_email, dynamic_template_data=data, template_id=template_id)
    
        return jsonify({
            "message": "Reference has been submitted successfully.",
            "status": "success",
            "reference": {
                "ref_id": reference.id,
                "ref_name": reference.ref_name,
                "ref_email": reference.ref_email,
                "reasons_gscf_makes_a_good_partner": reference.reasons_gscf_makes_a_good_partner,
                "good_match_for_gscf": reference.good_match_for_gscf,
                "is_approved": reference.is_approved
            }
        })
    
    else:
        return jsonify({
            "message": "There is no such reference id",
            "status": "failed"
        })

@references_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json

    gsc = data.get('gsc_id')
    ref_name = data.get('ref_name')
    ref_email = data.get('ref_email')

    reference = Reference(
            gsc = gsc,
            ref_name = ref_name,
            ref_email = ref_email
        )
    if reference.save():
        gsc = reference.gsc
        template_id = "d-6af1d902e5544dc68eeab4fe99809219"
        data = {
                "gscf_name": gsc.name,
                "ref_name": reference.ref_name,
                "ref_url": f"https://www.matchesup.com/good-single-christian-friend/{gsc.uuid}/{reference.id}/reference/{reference.ref_name}"
            }

        send_reference_email = sendgrid(to_email=reference.ref_email, dynamic_template_data=data, template_id=template_id)

        return jsonify({
            "message": "Reference has been submitted successfully.",
            "status": "success",
            "reference": {
                "ref_id": reference.id,
                "ref_name": reference.ref_name,
                "ref_email": reference.ref_email,
                "reasons_gscf_makes_a_good_partner": reference.reasons_gscf_makes_a_good_partner,
                "good_match_for_gscf": reference.good_match_for_gscf,
                "is_approved": reference.is_approved
            }
        })
    elif reference.errors != 0:
        return jsonify({
            "message": [error for error in reference.errors],
            "status": "failed"
        })

@references_api_blueprint.route('/<id>', methods=['GET'])
def show(id):
    reference = Reference.get_or_none(Reference.id == id)

    if reference:
        gsc = reference.gsc

        return jsonify({
            "gscf_name": gsc.name,
            "gscf_email": gsc.email,
            "ref_id": reference.id,
            "ref_name": reference.ref_name,
            "ref_email": reference.ref_email,
            "reasons_gscf_makes_a_good_partner": reference.reasons_gscf_makes_a_good_partner,
            "good_match_for_gscf": reference.good_match_for_gscf,
            "is_approved": reference.is_approved
        })
    
    else:
        return jsonify({
            "message": "There is no such reference"
        })

@references_api_blueprint.route('/<ref_id>', methods=['POST'])
def update(ref_id):
    update_reference = Reference.get_or_none(Reference.id == ref_id)

    data = request.json

    reasons_gscf_makes_a_good_partner = data.get('reasons_gscf_makes_a_good_partner')
    good_match_for_gscf = data.get('good_match_for_gscf')

    if (reasons_gscf_makes_a_good_partner != "" and good_match_for_gscf != ""):
        update_reference.reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner
        update_reference.good_match_for_gscf = good_match_for_gscf

        if update_reference.save(only=[
            Reference.reasons_gscf_makes_a_good_partner,
            Reference.good_match_for_gscf,
            ]):

            gsc = update_reference.gsc
            template_id = "d-b0df696531cb4b8fb4234b6ff1a05aa0"
            data = {
                    "gscf_name": gsc.name,
                    "ref_name": update_reference.ref_name,
                    "edit_url": f"https://www.matchesup.com/good-single-christian-friend/{gsc.uuid}/edit"
                    }
    
            send_approve_reference_email = sendgrid(to_email=gsc.email, dynamic_template_data=data, template_id=template_id)

            return jsonify({
                "message": "Successfully updated reference!",
                "status": "success",
                "reference": {
                    "ref_name": update_reference.ref_name,
                    "ref_email": update_reference.ref_email,
                    "reasons_gscf_makes_a_good_partner": update_reference.reasons_gscf_makes_a_good_partner,
                    "good_match_for_gscf": update_reference.good_match_for_gscf,
                    "is_approved": update_reference.is_approved
                }
            })

        elif update_reference.errors != 0:
            return jsonify({
                "message": [error for error in update_reference.errors],
                "status": "failed"
            })
    
    else:
        return jsonify({
            "message": "At least on field must be filled",
            "status": "failed"
        })

@references_api_blueprint.route('/edit/<ref_id>', methods=['POST'])
def edit(ref_id):
    edit_reference = Reference.get_or_none(Reference.id == ref_id)

    data = request.json

    reasons_gscf_makes_a_good_partner = data.get('reasons_gscf_makes_a_good_partner')
    good_match_for_gscf = data.get('good_match_for_gscf')
    is_approved = data.get('is_approved')

    if (reasons_gscf_makes_a_good_partner != "" and good_match_for_gscf != ""):
        edit_reference.reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner
        edit_reference.good_match_for_gscf = good_match_for_gscf
        edit_reference.is_approved = is_approved

        if edit_reference.save(only=[
            Reference.reasons_gscf_makes_a_good_partner,
            Reference.good_match_for_gscf,
            Reference.is_approved
            ]):
            return jsonify({
                "message": "Successfully updated reference!",
                "status": "success",
                "reference": {
                    "ref_name": edit_reference.ref_name,
                    "ref_email": edit_reference.ref_email,
                    "reasons_gscf_makes_a_good_partner": edit_reference.reasons_gscf_makes_a_good_partner,
                    "good_match_for_gscf": edit_reference.good_match_for_gscf,
                    "is_approved": edit_reference.is_approved
                }
            })

        elif edit_reference.errors != 0:
            return jsonify({
                "message": [error for error in edit_reference.errors],
                "status": "failed"
            })
    
    else:
        return jsonify({
            "message": "At least on field must be filled",
            "status": "failed"
        })