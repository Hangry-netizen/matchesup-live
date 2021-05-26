from flask import Blueprint, jsonify, request
from models.reference import Reference
from models.gsc import Gsc

references_api_blueprint = Blueprint('references_api',
                             __name__)

@references_api_blueprint.route('/', methods=['GET'])
def index():
    references = Reference.select()
    return jsonify([{
        "ref_name": reference.ref_name,
        "ref_email": reference.ref_email,
        "reasons_gscf_makes_a_good_partner": reference.reasons_gscf_makes_a_good_partner,
        "good_match_for_gscf": reference.good_match_for_gscf,
        "is_approved": reference.is_approved
    } for reference in references])
    
@references_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json

    gsc = data.get('gsc')
    ref_name = data.get('ref_name')
    ref_email = data.get('ref_email')
    reasons_gscf_makes_a_good_partner = data.get('reasons_gscf_makes_a_good_partner')
    good_match_for_gscf = data.get('good_match_for_gscf')

    reference = Reference(
            gsc = gsc,
            ref_name = ref_name,
            ref_email = ref_email,
            reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner,
            good_match_for_gscf = good_match_for_gscf
        )
    if reference.save():
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

    return jsonify({
        "ref_id": reference.id,
        "ref_name": reference.ref_name,
        "ref_email": reference.ref_email,
        "reasons_gscf_makes_a_good_partner": reference.reasons_gscf_makes_a_good_partner,
        "good_match_for_gscf": reference.good_match_for_gscf,
        "is_approved": reference.is_approved
    })

@references_api_blueprint.route('/<ref_id>', methods=['POST'])
def update(ref_id):
    update_reference = Reference.get_or_none(Reference.id == ref_id)

    data = request.json

    reasons_gscf_makes_a_good_partner = data.get('reasons_gscf_makes_a_good_partner')
    good_match_for_gscf = data.get('good_match_for_gscf')
    is_approved = data.get('is_approved')

    if (reasons_gscf_makes_a_good_partner != "" and good_match_for_gscf != ""):
        update_reference.reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner
        update_reference.good_match_for_gscf = good_match_for_gscf
        update_reference.is_approved = is_approved

        if update_reference.save(only=[
            Reference.reasons_gscf_makes_a_good_partner,
            Reference.good_match_for_gscf,
            Reference.is_approved
            ]):
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
