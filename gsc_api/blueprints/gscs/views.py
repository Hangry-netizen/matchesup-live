from flask import Blueprint, jsonify, request
from models.gsc import *
from models.hello import *
from helpers import sendgrid

gscs_api_blueprint = Blueprint('gscs_api',
                             __name__)

@gscs_api_blueprint.route('/', methods=['GET'])
def index():
    gscs = Gsc.select()
    return jsonify([{
        "uuid": gsc.uuid,
        "id": gsc.id,
        "name": gsc.name,
        "email": gsc.email,
        "gender": gsc.gender,
        "year_of_birth": gsc.year_of_birth,
        "height": gsc.height,
        "languages": gsc.languages,
        "nationality": gsc.nationality,
        "city": gsc.city,
        "country": gsc.country,
        "descriptive_words": gsc.descriptive_words,
        "mbti": gsc.mbti,
        "enneagram": gsc.enneagram,
        "disc": gsc.disc,
        "strengths_finder": gsc.strengths_finder,
        "favorite_topics": gsc.favorite_topics,
        "chill_activities": gsc.chill_activities,
        "do": gsc.do,
        "skills_and_talents": gsc.skills_and_talents,
        "growth_and_development": gsc.growth_and_development,
        "spiritual_gifts": gsc.spiritual_gifts,
        "spiritual_maturity": gsc.spiritual_maturity,
        "church_background": gsc.church_background,
        "reasons_gscf_makes_a_good_partner": gsc.reasons_gscf_makes_a_good_partner,
        "good_match_for_gscf": gsc.good_match_for_gscf,
        "moving_to_a_different_town": gsc.moving_to_a_different_town,
        "moving_to_a_different_country": gsc.moving_to_a_different_country,
        "has_been_married_or_has_kids": gsc.has_been_married_or_has_kids,
        "want_to_have_kids": gsc.want_to_have_kids,
        "important_info_to_know": gsc.important_info_to_know,
        "alias": gsc.alias,
        "consent": gsc.consent,
        "social_media_profile_link": gsc.social_media_profile_link,
        "preferred_contact_method": gsc.preferred_contact_method,
        "contact_info": gsc.contact_info,
        "notification_frequency": gsc.notification_frequency,
        "what_is_important_to_me": gsc.what_is_important_to_me,
        "is_approved": gsc.is_approved,
        "is_active": gsc.is_active,
        "is_activated": gsc.is_activated,
        "ff_name": gsc.ff_name,
        "ff_email": gsc.ff_email,
        "monthly_hellos": gsc.monthly_hellos
        }
        for gsc in gscs
    ])

@gscs_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    gender = data.get('gender')
    year_of_birth = data.get('year_of_birth')
    height = data.get('height')
    languages = data.get('languages')
    nationality = data.get('nationality')
    city = data.get('city')
    country = data.get('country')
    descriptive_words = data.get('descriptive_words')
    mbti = data.get('mbti')
    enneagram = data.get('enneagram')
    disc = data.get('disc')
    strengths_finder = data.get('strengths_finder')
    favorite_topics = data.get('favorite_topics')
    chill_activities = data.get('chill_activities')
    do = data.get('do')
    skills_and_talents = data.get('skills_and_talents')
    growth_and_development = data.get('growth_and_development')
    spiritual_gifts = data.get('spiritual_gifts')
    spiritual_maturity = data.get('spiritual_maturity')
    church_background = data.get('church_background')
    reasons_gscf_makes_a_good_partner = data.get('reasons_gscf_makes_a_good_partner')
    good_match_for_gscf = data.get('good_match_for_gscf')
    moving_to_a_different_town = data.get('moving_to_a_different_town')
    moving_to_a_different_country = data.get('moving_to_a_different_country')
    has_been_married_or_has_kids = data.get('has_been_married_or_has_kids')
    want_to_have_kids = data.get('want_to_have_kids')
    important_info_to_know = data.get('important_info_to_know')
    alias = data.get('alias')
    ff_name = data.get('ff_name')
    ff_email = data.get('ff_email')

    if name and email:
        gsc = Gsc(
                name = name,
                email = email,
                gender = gender,
                year_of_birth = year_of_birth,
                height = height,
                languages = languages,
                nationality = nationality,
                city = city,
                country = country,
                descriptive_words = descriptive_words,
                mbti = mbti,
                enneagram = enneagram,
                disc = disc,
                strengths_finder = strengths_finder,
                favorite_topics = favorite_topics,
                chill_activities = chill_activities,
                do = do,
                skills_and_talents = skills_and_talents,
                growth_and_development = growth_and_development,
                spiritual_gifts = spiritual_gifts,
                spiritual_maturity = spiritual_maturity,
                church_background = church_background,
                reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner,
                good_match_for_gscf = good_match_for_gscf,
                moving_to_a_different_town = moving_to_a_different_town,
                moving_to_a_different_country = moving_to_a_different_country,
                has_been_married_or_has_kids = has_been_married_or_has_kids,
                want_to_have_kids = want_to_have_kids,
                important_info_to_know = important_info_to_know,
                alias = alias,
                ff_name = ff_name,
                ff_email = ff_email,
        )
        if gsc.save():
            email = gsc.email
            template_id="d-fcb0e7483d4448319fa772341765a581"
            data = {
                "gscf_name": gsc.name,
                "ff_name": gsc.ff_name,
                "ff_email": gsc.ff_email,
                "consent_url": f"https://www.matchesup.com/good-single-christian-friend/{gsc.uuid}/consent",
                "gsc_profile_link": f"https://www.matchesup.com/good-single-christian-friend/{gsc.uuid}"
            }

            send_gsc_consent_email = sendgrid(to_email=email, dynamic_template_data=data, template_id=template_id)

            return jsonify({
                "message": "Successfully added a new gsc",
                "status": "success",
                "gsc": {
                    "uuid": gsc.uuid,
                    "name": gsc.name,
                    "email": gsc.email
                }
            })
        elif gsc.errors != 0:
            return jsonify({
                "message": [error for error in gsc.errors],
                "status": "failed"
            })
    else:
        return jsonify({
            "message": "All fields are required!",
            "status": "failed"
        })

@gscs_api_blueprint.route('/<uuid>', methods=['GET'])
def show(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    if gsc:
        return jsonify({
            "uuid": gsc.uuid,
            "id": gsc.id,
            "name": gsc.name,
            "email": gsc.email,
            "gender": gsc.gender,
            "year_of_birth": gsc.year_of_birth,
            "height": gsc.height,
            "languages": gsc.languages,
            "nationality": gsc.nationality,
            "city": gsc.city,
            "country": gsc.country,
            "descriptive_words": gsc.descriptive_words,
            "mbti": gsc.mbti,
            "enneagram": gsc.enneagram,
            "disc": gsc.disc,
            "strengths_finder": gsc.strengths_finder,
            "favorite_topics": gsc.favorite_topics,
            "chill_activities": gsc.chill_activities,
            "do": gsc.do,
            "skills_and_talents": gsc.skills_and_talents,
            "growth_and_development": gsc.growth_and_development,
            "spiritual_gifts": gsc.spiritual_gifts,
            "spiritual_maturity": gsc.spiritual_maturity,
            "church_background": gsc.church_background,
            "reasons_gscf_makes_a_good_partner": gsc.reasons_gscf_makes_a_good_partner,
            "good_match_for_gscf": gsc.good_match_for_gscf,
            "moving_to_a_different_town": gsc.moving_to_a_different_town,
            "moving_to_a_different_country": gsc.moving_to_a_different_country,
            "has_been_married_or_has_kids": gsc.has_been_married_or_has_kids,
            "want_to_have_kids": gsc.want_to_have_kids,
            "important_info_to_know": gsc.important_info_to_know,
            "alias": gsc.alias,
            "consent": gsc.consent,
            "social_media_profile_link": gsc.social_media_profile_link,
            "preferred_contact_method": gsc.preferred_contact_method,
            "contact_info": gsc.contact_info,
            "notification_frequency": gsc.notification_frequency,
            "what_is_important_to_me": gsc.what_is_important_to_me,
            "is_approved": gsc.is_approved,
            "is_active": gsc.is_active,
            "is_activated": gsc.is_activated,
            "ff_name": gsc.ff_name,
            "ff_email": gsc.ff_email,
            "monthly_hellos": gsc.monthly_hellos,
            "suggested": gsc.suggested,
            "maybe": gsc.maybe,
            "contacted": gsc.contacted,
            "deleted": gsc.deleted
        })

    else:
        return jsonify({
            "message": "There is no such GSC",
            "status":"failed"
        })

@gscs_api_blueprint.route('/<uuid>', methods=['POST'])
def update(uuid):
    update_gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    name = data.get('name')
    gender = data.get('gender')
    year_of_birth = data.get('year_of_birth')
    height = data.get('height')
    languages = data.get('languages')
    nationality = data.get('nationality')
    city = data.get('city')
    country = data.get('country')
    descriptive_words = data.get('descriptive_words')
    mbti = data.get('mbti')
    enneagram = data.get('enneagram')
    disc = data.get('disc')
    strengths_finder = data.get('strengths_finder')
    favorite_topics = data.get('favorite_topics')
    chill_activities = data.get('chill_activities')
    do = data.get('do')
    skills_and_talents = data.get('skills_and_talents')
    growth_and_development = data.get('growth_and_development')
    spiritual_gifts = data.get('spiritual_gifts')
    spiritual_maturity = data.get('spiritual_maturity')
    church_background = data.get('church_background')
    reasons_gscf_makes_a_good_partner = data.get('reasons_gscf_makes_a_good_partner')
    good_match_for_gscf = data.get('good_match_for_gscf')
    moving_to_a_different_town = data.get('moving_to_a_different_town')
    moving_to_a_different_country = data.get('moving_to_a_different_country')
    has_been_married_or_has_kids = data.get('has_been_married_or_has_kids')
    want_to_have_kids = data.get('want_to_have_kids')
    important_info_to_know = data.get('important_info_to_know')
    alias = data.get('alias')
    ff_name = data.get('ff_name')
    ff_email = data.get('ff_email')
    consent = data.get('consent')
    social_media_profile_link = data.get('social_media_profile_link') 
    preferred_contact_method = data.get('preferred_contact_method') 
    contact_info = data.get('contact_info') 
    notification_frequency = data.get('notification_frequency')
    what_is_important_to_me = data.get('what_is_important_to_me') 
    is_approved = data.get('is_approved') 
    is_active = data.get('is_active')
    monthly_hellos = data.get('monthly_hellos')

    if (
    name != "" or 
    year_of_birth != "" or
    height != "" or
    languages != "" or
    nationality != "" or
    city != "" or
    country != "" or
    descriptive_words != "" or
    mbti != "" or
    enneagram != "" or
    disc != "" or
    strengths_finder != "" or
    favorite_topics != "" or
    chill_activities != "" or
    do != "" or
    skills_and_talents != "" or
    growth_and_development != "" or
    spiritual_gifts != "" or
    spiritual_maturity != "" or
    church_background != "" or
    reasons_gscf_makes_a_good_partner != "" or
    good_match_for_gscf != "" or
    moving_to_a_different_town != "" or
    moving_to_a_different_country != "" or
    has_been_married_or_has_kids != "" or
    want_to_have_kids != "" or
    important_info_to_know != "" or
    alias != "" or
    consent != "" or
    social_media_profile_link != "" or 
    preferred_contact_method != "" or 
    contact_info != "" or 
    notification_frequency != "" or
    what_is_important_to_me != "" or
    ff_name != "" or 
    ff_email != "" or
    is_approved != "" or 
    is_active != ""):
        update_gsc.name = name
        update_gsc.year_of_birth = year_of_birth
        update_gsc.height = height
        update_gsc.languages = languages
        update_gsc.nationality = nationality
        update_gsc.city = city
        update_gsc.country = country
        update_gsc.descriptive_words = descriptive_words
        update_gsc.mbti = mbti
        update_gsc.enneagram = enneagram
        update_gsc.disc = disc
        update_gsc.strengths_finder = strengths_finder
        update_gsc.favorite_topics = favorite_topics
        update_gsc.chill_activities = chill_activities
        update_gsc.do = do
        update_gsc.skills_and_talents = skills_and_talents
        update_gsc.growth_and_development = growth_and_development
        update_gsc.spiritual_gifts = spiritual_gifts
        update_gsc.spiritual_maturity = spiritual_maturity
        update_gsc.church_background = church_background
        update_gsc.reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner
        update_gsc.good_match_for_gscf = good_match_for_gscf
        update_gsc.moving_to_a_different_town = moving_to_a_different_town
        update_gsc.moving_to_a_different_country = moving_to_a_different_country
        update_gsc.has_been_married_or_has_kids = has_been_married_or_has_kids
        update_gsc.want_to_have_kids = want_to_have_kids
        update_gsc.important_info_to_know = important_info_to_know
        update_gsc.alias = alias
        update_gsc.consent = consent
        update_gsc.social_media_profile_link = social_media_profile_link 
        update_gsc.preferred_contact_method = preferred_contact_method 
        update_gsc.contact_info = contact_info 
        update_gsc.notification_frequency = notification_frequency
        update_gsc.what_is_important_to_me = what_is_important_to_me
        update_gsc.ff_name = ff_name
        update_gsc.ff_email = ff_email
        update_gsc.is_approved = is_approved 
        update_gsc.is_active = is_active
        update_gsc.monthly_hellos = monthly_hellos

        if update_gsc.save():
            return jsonify({
                "message": "Successfully updated your profile!",
                "status": "success"
            })

        elif update_gsc.errors != 0:
            return jsonify({
                "message": [error for error in update_gsc.errors],
                "status": "failed"
            })
    
    else:
        return jsonify({
            "message": "At least on field must be filled",
            "status": "failed"
        })
        
@gscs_api_blueprint.route('/consent/<uuid>', methods=['POST'])
def consent(uuid):
    update_gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    consent = data.get('consent')
    social_media_profile_link = data.get('social_media_profile_link') 
    preferred_contact_method = data.get('preferred_contact_method') 
    contact_info = data.get('contact_info') 
    notification_frequency = data.get('notification_frequency')
    what_is_important_to_me = data.get('what_is_important_to_me') 

    if (
    consent != "" or
    social_media_profile_link != "" or 
    preferred_contact_method != "" or 
    contact_info != "" or 
    notification_frequency != "" or
    what_is_important_to_me != ""):
        update_gsc.consent = consent
        update_gsc.social_media_profile_link = social_media_profile_link 
        update_gsc.preferred_contact_method = preferred_contact_method 
        update_gsc.contact_info = contact_info 
        update_gsc.notification_frequency = notification_frequency
        update_gsc.what_is_important_to_me = what_is_important_to_me

        if update_gsc.save(only=[
            Gsc.consent, 
            Gsc.social_media_profile_link,
            Gsc.preferred_contact_method,
            Gsc.contact_info,
            Gsc.notification_frequency,
            Gsc.what_is_important_to_me
            ]):
            
            return jsonify({
                "message": "Successfully submitted consent!",
                "status": "success",
                 "gsc": {
                    "uuid": update_gsc.uuid,
                    "name": update_gsc.name,
                    "alias": update_gsc.alias
                }
            })

        elif update_gsc.errors != 0:
            return jsonify({
                "message": [error for error in update_gsc.errors],
                "status": "failed"
            })
    
    else:
        return jsonify({
            "message": "At least on field must be filled",
            "status": "failed"
        })

@gscs_api_blueprint.route('/approve/<uuid>', methods=['POST'])
def approve(uuid):
    approve_gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    is_approved = data.get('is_approved') 

    if is_approved:
        approve_gsc.is_approved = is_approved 

        if approve_gsc.save(only=[Gsc.is_approved]):
            email = approve_gsc.email
            template_id = "d-e0573f50445145e9ba6542744ff4053a"
            data = {
                "gscf_name": approve_gsc.name,
                "edit_url": f"https://www.matchesup.com/good-single-christian-friend/{approve_gsc.uuid}"
            }

            send_approved_email = sendgrid(to_email=email, dynamic_template_data=data, template_id=template_id)

            return jsonify({
                "message": "Successfully updated GSCF status!",
                "status": "success",
                "gsc": {
                    "uuid": approve_gsc.uuid,
                    "name": approve_gsc.name,
                    "is_approved": approve_gsc.is_approved
                }
            })

        elif approve.errors != 0:
            return jsonify({
                "message": [error for error in approve.errors],
                "status": "failed"
            })
    
    else:
        return jsonify({
            "message": "At least on field must be filled",
            "status": "failed"
        })

@gscs_api_blueprint.route('/status/<uuid>', methods=['POST'])
def status(uuid):
    status = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    is_approved = data.get('is_approved') 
    is_active = data.get('is_active')
    is_activated = data.get('is_activated')

    if (
    is_approved != "" or 
    is_active != "" or
    is_activated != ""):
        status.is_approved = is_approved 
        status.is_active = is_active 
        status.is_activated = is_activated

        if status.save(only=[
            Gsc.is_approved, 
            Gsc.is_active,
            Gsc.is_activated
            ]):

            return jsonify({
                "message": "Successfully updated GSCF status!",
                "status": "success",
                 "gsc": {
                    "uuid": status.uuid,
                    "name": status.name,
                    "is_approved": status.is_approved,
                    "is_active": status.is_active,
                    "is_activated": status.is_activated
                 }
            })

        elif status.errors != 0:
            return jsonify({
                "message": [error for error in status.errors],
                "status": "failed"
            })
    
    else:
        return jsonify({
            "message": "At least on field must be filled",
            "status": "failed"
        })

@gscs_api_blueprint.route('/said-hi/<uuid>', methods=["GET"])
def said_hi(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)
    hellos = gsc.said_hi

    response = []
    duplicate_check = []

    for hello in hellos:
        hi_recipient = hello.hi_recipient
        if hello.removed == False:
            data = {
                "hello_id": hello.id,
                "hello_contacted": hello.contacted,
                "id": hi_recipient.id,
                "name": hi_recipient.name,
                "year_of_birth": hi_recipient.year_of_birth,
                "height": hi_recipient.height,
                "languages": hi_recipient.languages, 
                "nationality": hi_recipient.nationality, 
                "city": hi_recipient.city, 
                "country": hi_recipient.country, 
                "descriptive_words": hi_recipient.descriptive_words,
                "mbti": hi_recipient.mbti, 
                "enneagram": hi_recipient.enneagram,
                "disc": hi_recipient.disc,
                "strengths_finder": hi_recipient.strengths_finder,
                "favorite_topics": hi_recipient.favorite_topics,
                "chill_activities": hi_recipient.chill_activities,
                "do": hi_recipient.do,
                "skills_and_talents": hi_recipient.skills_and_talents,
                "growth_and_development": hi_recipient.growth_and_development,
                "spiritual_gifts": hi_recipient.spiritual_gifts,
                "spiritual_maturity": hi_recipient.spiritual_maturity,
                "church_background": hi_recipient.church_background,
                "reasons_gscf_makes_a_good_partner": hi_recipient.reasons_gscf_makes_a_good_partner,
                "good_match_for_gscf": hi_recipient.good_match_for_gscf,
                "moving_to_a_different_town": hi_recipient.moving_to_a_different_town,
                "moving_to_a_different_country": hi_recipient.moving_to_a_different_country,
                "has_been_married_or_has_kids": hi_recipient.has_been_married_or_has_kids,
                "want_to_have_kids": hi_recipient.want_to_have_kids,
                "preferred_contact_method": hi_recipient.preferred_contact_method,
                "contact_info": hi_recipient.contact_info,
                "important_info_to_know": hi_recipient.important_info_to_know,
                "alias": hi_recipient.alias,
                "social_media_profile_link": hi_recipient.social_media_profile_link, 
                "preferred_contact_method": hi_recipient.preferred_contact_method,
                "contact_info": hi_recipient.contact_info,
                "what_is_important_to_me": hi_recipient.what_is_important_to_me
            }
            if hi_recipient.id not in duplicate_check:
                response.append(data)
                duplicate_check.append(hi_recipient.id)
    
    return jsonify(response)

@gscs_api_blueprint.route('/hi-recipient/<uuid>', methods=["GET"])
def hi_recipient(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)
    hellos = gsc.hi_recipient

    response = []
    duplicate_check = []

    for hello in hellos:
        said_hi = hello.said_hi
        if hello.removed == False:
            data = {
                "hello_id": hello.id,
                "hello_contacted": hello.contacted,
                "id": said_hi.id,
                "name": said_hi.name,
                "year_of_birth": said_hi.year_of_birth,
                "height": said_hi.height,
                "languages": said_hi.languages, 
                "nationality": said_hi.nationality, 
                "city": said_hi.city,
                "country": said_hi.country, 
                "descriptive_words": said_hi.descriptive_words,
                "mbti": said_hi.mbti, 
                "enneagram": said_hi.enneagram,
                "disc": said_hi.disc,
                "strengths_finder": said_hi.strengths_finder,
                "favorite_topics": said_hi.favorite_topics,
                "chill_activities": said_hi.chill_activities,
                "do": said_hi.do,
                "skills_and_talents": said_hi.skills_and_talents,
                "growth_and_development": said_hi.growth_and_development,
                "spiritual_gifts": said_hi.spiritual_gifts,
                "spiritual_maturity": said_hi.spiritual_maturity,
                "church_background": said_hi.church_background,
                "reasons_gscf_makes_a_good_partner": said_hi.reasons_gscf_makes_a_good_partner,
                "good_match_for_gscf": said_hi.good_match_for_gscf,
                "moving_to_a_different_town": said_hi.moving_to_a_different_town,
                "moving_to_a_different_country": said_hi.moving_to_a_different_country,
                "has_been_married_or_has_kids": said_hi.has_been_married_or_has_kids,
                "want_to_have_kids": said_hi.want_to_have_kids,
                "preferred_contact_method": said_hi.preferred_contact_method,
                "contact_info": said_hi.contact_info,
                "important_info_to_know": said_hi.important_info_to_know,
                "alias": said_hi.alias,
                "social_media_profile_link": said_hi.social_media_profile_link, 
                "preferred_contact_method": said_hi.preferred_contact_method,
                "contact_info": said_hi.contact_info,
                "what_is_important_to_me": said_hi.what_is_important_to_me
            }
            if said_hi.id not in duplicate_check:
                response.append(data)
                duplicate_check.append(said_hi.id)
    
    return jsonify(response)
@gscs_api_blueprint.route('/database-display/<uuid>', methods=["GET"])
def database_display(uuid):
    currentGsc = Gsc.get_or_none(Gsc.uuid == uuid)
    gscs = Gsc.select()

    hi_recipient_hellos = currentGsc.hi_recipient
    said_hi_hellos = currentGsc.said_hi

    response = []
    duplicate_check = []

    for gsc in gscs:
        for hello in said_hi_hellos:
            if hello.hi_recipient == gsc:
                if hello.removed == False:
                    if gsc.is_active:
                        reasons_gscf_makes_a_good_partner = ""
                        good_match_for_gscf = ""
                        if gsc.references:
                            refs = gsc.references
                            for ref in refs:
                                if ref.is_approved:
                                    if ref.reasons_gscf_makes_a_good_partner and ref.good_match_for_gscf:
                                        reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + ref.reasons_gscf_makes_a_good_partner
                                        good_match_for_gscf = good_match_for_gscf + " " + ref.good_match_for_gscf
                                        reasons_gscf_makes_a_good_partner.strip()
                                        good_match_for_gscf.strip()
                            
                            reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + gsc.reasons_gscf_makes_a_good_partner
                            good_match_for_gscf = good_match_for_gscf + " " + gsc.good_match_for_gscf
                            reasons_gscf_makes_a_good_partner.strip()
                            good_match_for_gscf.strip()
                        else:
                            reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + gsc.reasons_gscf_makes_a_good_partner
                            good_match_for_gscf = good_match_for_gscf + " " + gsc.good_match_for_gscf
                            reasons_gscf_makes_a_good_partner.strip()
                            good_match_for_gscf.strip()

                        data = {
                            "hello_id": hello.id,
                            "action": "said_hi",
                            "id": gsc.id,
                            "gender": gsc.gender,
                            "name": gsc.name,
                            "year_of_birth": gsc.year_of_birth,
                            "height": gsc.height,
                            "languages": gsc.languages, 
                            "nationality": gsc.nationality, 
                            "city": gsc.city,
                            "country": gsc.country, 
                            "descriptive_words": gsc.descriptive_words,
                            "mbti": gsc.mbti, 
                            "enneagram": gsc.enneagram,
                            "disc": gsc.disc,
                            "strengths_finder": gsc.strengths_finder,
                            "favorite_topics": gsc.favorite_topics,
                            "chill_activities": gsc.chill_activities,
                            "do": gsc.do,
                            "skills_and_talents": gsc.skills_and_talents,
                            "growth_and_development": gsc.growth_and_development,
                            "spiritual_gifts": gsc.spiritual_gifts,
                            "spiritual_maturity": gsc.spiritual_maturity,
                            "church_background": gsc.church_background,
                            "reasons_gscf_makes_a_good_partner": reasons_gscf_makes_a_good_partner,
                            "good_match_for_gscf": good_match_for_gscf,
                            "moving_to_a_different_town": gsc.moving_to_a_different_town,
                            "moving_to_a_different_country": gsc.moving_to_a_different_country,
                            "has_been_married_or_has_kids": gsc.has_been_married_or_has_kids,
                            "want_to_have_kids": gsc.want_to_have_kids,
                            "preferred_contact_method": gsc.preferred_contact_method,
                            "contact_info": gsc.contact_info,
                            "important_info_to_know": gsc.important_info_to_know,
                            "alias": gsc.alias,
                            "social_media_profile_link": gsc.social_media_profile_link, 
                            "preferred_contact_method": gsc.preferred_contact_method,
                            "contact_info": gsc.contact_info,
                            "what_is_important_to_me": gsc.what_is_important_to_me
                        }
                        if gsc.id not in duplicate_check:
                            response.append(data)
                            duplicate_check.append(gsc.id)
                else:
                    duplicate_check.append(gsc.id)
        
        for hello in hi_recipient_hellos:
            if hello.said_hi == gsc:
                if hello.removed == False:
                    if gsc.is_active:
                        reasons_gscf_makes_a_good_partner = ""
                        good_match_for_gscf = ""

                        if gsc.references:
                            refs = gsc.references
                            for ref in refs:
                                if ref.is_approved:
                                    if ref.reasons_gscf_makes_a_good_partner and ref.good_match_for_gscf:
                                        reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + ref.reasons_gscf_makes_a_good_partner
                                        good_match_for_gscf = good_match_for_gscf + " " + ref.good_match_for_gscf
                                        reasons_gscf_makes_a_good_partner.strip()
                                        good_match_for_gscf.strip()
                            
                            reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + gsc.reasons_gscf_makes_a_good_partner
                            good_match_for_gscf = good_match_for_gscf + " " + gsc.good_match_for_gscf
                            reasons_gscf_makes_a_good_partner.strip()
                            good_match_for_gscf.strip()
                        else:
                            reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + gsc.reasons_gscf_makes_a_good_partner
                            good_match_for_gscf = good_match_for_gscf + " " + gsc.good_match_for_gscf
                            reasons_gscf_makes_a_good_partner.strip()
                            good_match_for_gscf.strip()

                        data = {
                            "hello_id": hello.id,
                            "action": "hi_recipient",
                            "id": gsc.id,
                            "gender": gsc.gender,
                            "name": gsc.name,
                            "year_of_birth": gsc.year_of_birth,
                            "height": gsc.height,
                            "languages": gsc.languages, 
                            "nationality": gsc.nationality, 
                            "city": gsc.city,
                            "country": gsc.country, 
                            "descriptive_words": gsc.descriptive_words,
                            "mbti": gsc.mbti, 
                            "enneagram": gsc.enneagram,
                            "disc": gsc.disc,
                            "strengths_finder": gsc.strengths_finder,
                            "favorite_topics": gsc.favorite_topics,
                            "chill_activities": gsc.chill_activities,
                            "do": gsc.do,
                            "skills_and_talents": gsc.skills_and_talents,
                            "growth_and_development": gsc.growth_and_development,
                            "spiritual_gifts": gsc.spiritual_gifts,
                            "spiritual_maturity": gsc.spiritual_maturity,
                            "church_background": gsc.church_background,
                            "reasons_gscf_makes_a_good_partner": reasons_gscf_makes_a_good_partner,
                            "good_match_for_gscf": good_match_for_gscf,
                            "moving_to_a_different_town": gsc.moving_to_a_different_town,
                            "moving_to_a_different_country": gsc.moving_to_a_different_country,
                            "has_been_married_or_has_kids": gsc.has_been_married_or_has_kids,
                            "want_to_have_kids": gsc.want_to_have_kids,
                            "preferred_contact_method": gsc.preferred_contact_method,
                            "contact_info": gsc.contact_info,
                            "important_info_to_know": gsc.important_info_to_know,
                            "alias": gsc.alias,
                            "social_media_profile_link": gsc.social_media_profile_link, 
                            "preferred_contact_method": gsc.preferred_contact_method,
                            "contact_info": gsc.contact_info,
                            "what_is_important_to_me": gsc.what_is_important_to_me
                        }
                        if gsc.id not in duplicate_check:
                            response.append(data)
                            duplicate_check.append(gsc.id)
                else:
                    if gsc.id not in duplicate_check:
                            duplicate_check.append(gsc.id)
            
        if gsc.is_active and gsc.id not in duplicate_check:
            reasons_gscf_makes_a_good_partner = ""
            good_match_for_gscf = ""

            if gsc.references:
                refs = gsc.references
                for ref in refs:
                    if ref.is_approved:
                        if ref.reasons_gscf_makes_a_good_partner and ref.good_match_for_gscf:
                            reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + ref.reasons_gscf_makes_a_good_partner
                            good_match_for_gscf = good_match_for_gscf + " " + ref.good_match_for_gscf
                            reasons_gscf_makes_a_good_partner.strip()
                            good_match_for_gscf.strip()
                
                reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + gsc.reasons_gscf_makes_a_good_partner
                good_match_for_gscf = good_match_for_gscf + " " + gsc.good_match_for_gscf
                reasons_gscf_makes_a_good_partner.strip()
                good_match_for_gscf.strip()
            else:
                reasons_gscf_makes_a_good_partner = reasons_gscf_makes_a_good_partner + " " + gsc.reasons_gscf_makes_a_good_partner
                good_match_for_gscf = good_match_for_gscf + " " + gsc.good_match_for_gscf
                reasons_gscf_makes_a_good_partner.strip()
                good_match_for_gscf.strip()

            data = {
                "id": gsc.id,
                "gender": gsc.gender,
                "name": gsc.name,
                "year_of_birth": gsc.year_of_birth,
                "height": gsc.height,
                "languages": gsc.languages,
                "nationality": gsc.nationality, 
                "city": gsc.city,
                "country": gsc.country, 
                "descriptive_words": gsc.descriptive_words,
                "mbti": gsc.mbti, 
                "enneagram": gsc.enneagram,
                "disc": gsc.disc,
                "strengths_finder": gsc.strengths_finder,
                "favorite_topics": gsc.favorite_topics,
                "chill_activities": gsc.chill_activities,
                "do": gsc.do,
                "skills_and_talents": gsc.skills_and_talents,
                "growth_and_development": gsc.growth_and_development,
                "spiritual_gifts": gsc.spiritual_gifts,
                "spiritual_maturity": gsc.spiritual_maturity,
                "church_background": gsc.church_background,
                "reasons_gscf_makes_a_good_partner": reasons_gscf_makes_a_good_partner,
                "good_match_for_gscf": good_match_for_gscf,
                "moving_to_a_different_town": gsc.moving_to_a_different_town,
                "moving_to_a_different_country": gsc.moving_to_a_different_country,
                "has_been_married_or_has_kids": gsc.has_been_married_or_has_kids,
                "want_to_have_kids": gsc.want_to_have_kids,
                "preferred_contact_method": gsc.preferred_contact_method,
                "contact_info": gsc.contact_info,
                "important_info_to_know": gsc.important_info_to_know,
                "alias": gsc.alias,
                "social_media_profile_link": gsc.social_media_profile_link, 
                "preferred_contact_method": gsc.preferred_contact_method,
                "contact_info": gsc.contact_info,
                "what_is_important_to_me": gsc.what_is_important_to_me
            }
            if gsc.id not in duplicate_check:
                response.append(data)
                duplicate_check.append(gsc.id)

    return jsonify(response)

@gscs_api_blueprint.route('/monthly-hellos/<uuid>', methods=['POST'])
def monthly_hellos(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    monthly_hellos = data.get('monthly_hellos') 

    if (monthly_hellos != ""):
        gsc.monthly_hellos = monthly_hellos  

        if gsc.save(only=[Gsc.monthly_hellos]):

            return jsonify({
                "message": f"Successfully updated {gsc.name}'s monthly hellos!",
                "status": "success"
            })

        elif gsc.errors != 0:
            return jsonify({
                "message": [error for error in gsc.errors],
                "status": "failed"
            })
    
    else:
        return jsonify({
            "message": "At least on field must be filled",
            "status": "failed"
        })

@gscs_api_blueprint.route('/send-database/<uuid>', methods=['POST'])
def send_database(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    monthly_hellos = data.get('monthly_hellos') 

    if (monthly_hellos != ""):
        if gsc.is_active:
            gsc.monthly_hellos = monthly_hellos
            if gsc.save(only=[Gsc.monthly_hellos]):
                email = gsc.email
                template_id = "d-87bbcbdab62a406d99104e4b9731bc7a"
                data = {
                    "gscf_name": gsc.name,
                    "database_url": f"https://www.matchesup.com/good-single-christian-friend/{gsc.uuid}"
                }
    
                send_monthly_database = sendgrid(to_email=email, dynamic_template_data=data, template_id=template_id)
                
                if send_monthly_database:
                    return jsonify({
                        "message": f"Successfully sent monthly database to {gsc.name}",
                        "status": "success"
                    })
                        
                else:
                    return jsonify({
                        "message": f"Failed to send monthly database to {gsc.name}",
                        "status": "failed"
                    })
            else:
                return jsonify({
                    "message": "Failed to save monthly hellos",
                    "status": "failed"
                })
        else:
            return jsonify({
                "message": "GSC is inactive",
                "status": "failed"
            })
    else:
        return jsonify({
            "message": "monthly_hellos field is empty",
            "status": "failed"
        })


@gscs_api_blueprint.route('/send-gscs-monthly-database', methods=['POST'])
def send_gscs_monthly_database():
    gscs = Gsc.select()

    response = []

    data = request.json

    monthly_hellos = data.get('monthly_hellos') 

    if (monthly_hellos != ""):
        for gsc in gscs:
            if gsc.is_active:
                gsc.monthly_hellos = monthly_hellos
                if gsc.save(only=[Gsc.monthly_hellos]):
                    email = gsc.email
                    template_id = "d-87bbcbdab62a406d99104e4b9731bc7a"
                    data = {
                        "gscf_name": gsc.name,
                        "database_url": f"https://www.matchesup.com/good-single-christian-friend/{gsc.uuid}"
                    }
        
                    send_monthly_database = sendgrid(to_email=email, dynamic_template_data=data, template_id=template_id)
                    
                    if send_monthly_database:
                        data = {
                            "message": f"Successfully sent monthly database to {gsc.name}",
                            "status": "success"
                        }
                        
                        response.append(data)
        
                    else:
                        data = {
                            "message": f"Failed to send monthly database to {gsc.name}",
                            "status": "failed"
                        }
        
                        response.append(data)
        
        return jsonify(response)

@gscs_api_blueprint.route('/send-ffs-monthly-email', methods=['POST'])
def send_ffs_monthly_email():
    gscs = Gsc.select()

    response = []

    duplicate_check = []

    for gsc in gscs:
        if gsc.is_active and gsc.ff_email not in duplicate_check:
            email = gsc.ff_email
            template_id = "d-2e75b4a841eb4f8daf8cc426ea5f7c6c"
            data = {
                "ff_name": gsc.ff_name
            }

            send_ff_monthly_email = sendgrid(to_email=email, dynamic_template_data=data, template_id=template_id)
            
            if send_ff_monthly_email:
                data = {
                    "message": f"Successfully sent monthly email to {gsc.ff_name} at {gsc.ff_email}",
                    "status": "success"
                }
                
                response.append(data)
                duplicate_check.append(gsc.ff_email)

            else:
                data = {
                    "message": f"Failed to send monthly email to {gsc.ff_name} at {gsc.ff_email}",
                    "status": "failed"
                }

                response.append(data)
    
    return jsonify(response)

@gscs_api_blueprint.route('/suggested/<uuid>', methods=['POST'])
def append_suggested(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    suggested = data.get('suggested') 

    if suggested:
        
        if gsc.suggested:
            if suggested not in gsc.suggested:
                gsc.suggested.append(suggested)
                if gsc.save(only=[Gsc.suggested]):
                    return jsonify({
                        "message": f"Successfully updated {gsc.name}'s suggested list!",
                        "status": "success"
                    })
    
                elif gsc.errors != 0:
                    return jsonify({
                        "message": [error for error in gsc.errors],
                        "status": "failed"
                    })
            else:
                 return jsonify({
                        "message": f"Failed to append because of duplication",
                        "status": "failed"
                    })

        else:
            gsc.suggested = [suggested]
            if gsc.save(only=[Gsc.suggested]):
                return jsonify({
                    "message": f"Successfully updated {gsc.name}'s suggested list!",
                    "status": "success"
                })

            elif gsc.errors != 0:
                return jsonify({
                    "message": [error for error in gsc.errors],
                    "status": "failed"
                })
    
    else:
        return jsonify({
            "message": "Suggested field is empty",
            "status": "failed"
        })

@gscs_api_blueprint.route('/maybe/<uuid>', methods=['POST'])
def append_maybe(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    maybe = data.get('maybe') 

    if maybe:
        
        if gsc.maybe:
            if maybe not in gsc.maybe:
                gsc.maybe.append(maybe)
                if gsc.save(only=[Gsc.maybe]):
                    return jsonify({
                        "message": f"Successfully updated {gsc.name}'s maybe list!",
                        "status": "success"
                    })
    
                elif gsc.errors != 0:
                    return jsonify({
                        "message": [error for error in gsc.errors],
                        "status": "failed"
                    })
            else:
                return jsonify({
                       "message": f"Failed to append because of duplication",
                       "status": "failed"
                   })

        else:
            gsc.maybe = [maybe]
            if gsc.save(only=[Gsc.maybe]):
                return jsonify({
                    "message": f"Successfully updated {gsc.name}'s maybe list!",
                    "status": "success"
                })

            elif gsc.errors != 0:
                return jsonify({
                    "message": [error for error in gsc.errors],
                    "status": "failed"
                })
    
    else:
        return jsonify({
            "message": "Maybe field is empty",
            "status": "failed"
        })

@gscs_api_blueprint.route('/contacted/<uuid>', methods=['POST'])
def append_contacted(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    contacted = data.get('contacted') 

    if contacted:
        
        if gsc.contacted:
            if contacted not in gsc.contacted:
                gsc.contacted.append(contacted)
                if gsc.save(only=[Gsc.contacted]):
                    return jsonify({
                        "message": f"Successfully updated {gsc.name}'s contacted list!",
                        "status": "success"
                    })
    
                elif gsc.errors != 0:
                    return jsonify({
                        "message": [error for error in gsc.errors],
                        "status": "failed"
                    })
            else:
                 return jsonify({
                        "message": f"Failed to append because of duplication",
                        "status": "failed"
                    })        

        else:
            gsc.contacted = [contacted]
            if gsc.save(only=[Gsc.contacted]):
                return jsonify({
                    "message": f"Successfully updated {gsc.name}'s contacted list!",
                    "status": "success"
                })

            elif gsc.errors != 0:
                return jsonify({
                    "message": [error for error in gsc.errors],
                    "status": "failed"
                })
    
    else:
        return jsonify({
            "message": "Contacted field is empty",
            "status": "failed"
        })

@gscs_api_blueprint.route('/remove-suggested/<uuid>', methods=['POST'])
def remove_suggested(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    remove_suggested = data.get('remove-suggested') 

    if remove_suggested:
        if gsc.suggested:
            gsc.suggested.remove(remove_suggested)
            if gsc.save(only=[Gsc.suggested]):
                return jsonify({
                    "message": f"Successfully removed suggestion from {gsc.name}'s suggestion list!",
                    "status": "success"
                })

            elif gsc.errors != 0:
                return jsonify({
                    "message": [error for error in gsc.errors],
                    "status": "failed"
                })

        else:
            return jsonify({
                "message": f"Suggestion list is empty",
                "status": "failed"
            })

    else:
        return jsonify({
            "message": "Remove-suggested field is empty",
            "status": "failed"
        })

@gscs_api_blueprint.route('/remove-maybe/<uuid>', methods=['POST'])
def remove_maybe(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    remove_maybe = data.get('remove-maybe') 

    if remove_maybe:
        if gsc.maybe:
            gsc.maybe.remove(remove_maybe)
            if gsc.save(only=[Gsc.maybe]):
                return jsonify({
                    "message": f"Successfully removed suggestion from {gsc.name}'s maybe list!",
                    "status": "success"
                })

            elif gsc.errors != 0:
                return jsonify({
                    "message": [error for error in gsc.errors],
                    "status": "failed"
                })

        else:
            return jsonify({
                "message": f"Maybe list is empty",
                "status": "failed"
            })

    else:
        return jsonify({
            "message": "Remove-maybe field is empty",
            "status": "failed"
        })

@gscs_api_blueprint.route('/delete-contacted/<uuid>', methods=['POST'])
def remove_contacted(uuid):
    gsc = Gsc.get_or_none(Gsc.uuid == uuid)

    data = request.json

    delete_contacted = data.get('delete-contacted') 

    if delete_contacted:
        if gsc.deleted:
            gsc.deleted.append(delete_contacted)
            if gsc.save(only=[Gsc.deleted]):
                return jsonify({
                    "message": f"Successfully deleted from {gsc.name}'s contacted list!",
                    "status": "success"
                })

            elif gsc.errors != 0:
                return jsonify({
                    "message": [error for error in gsc.errors],
                    "status": "failed"
                })

        else:
            gsc.deleted = [delete_contacted]
            if gsc.save(only=[Gsc.deleted]):
                return jsonify({
                    "message": f"Successfully removed suggestion from {gsc.name}'s contacted list!",
                    "status": "success"
                })

            elif gsc.errors != 0:
                return jsonify({
                    "message": [error for error in gsc.errors],
                    "status": "failed"
                })

    else:
        return jsonify({
            "message": "Remove-contacted field is empty",
            "status": "failed"
        })


@gscs_api_blueprint.route('/active-status/toggle/<id>', methods=['POST'])
def toggle_active(id):
    gsc = Gsc.get_or_none(Gsc.id == id)

    if gsc:
        gsc.is_active = not gsc.is_active

        if gsc.save(only=[Gsc.is_active]):
            return jsonify({
                "message": f"Successfully toggled {gsc.name}'s is_active status to {gsc.is_active}!",
                "active": gsc.is_active,
                "status": "success"
                })
    
        else:
            return jsonify({
                "message": f"Failed to toggle {gsc.name} is_active status",
                "status": "failed"
            })
    else:
        return jsonify({
                "message": f"There is no such gsc",
                "status": "failed"
            })

@gscs_api_blueprint.route('/delete/<id>', methods=['POST'])
def delete(id):
    gsc = Gsc.get_or_none(Gsc.id == id)

    if gsc:
        if gsc.delete_instance():
            return jsonify({
                "message": f"Successfully deleted {gsc.name} as a gsc",
                "status": "success"
            })
        else:
            return jsonify({
                "message": f"Failed to delete {gsc.name}'s profile",
                "status": "failed"
            })
    else:
        return jsonify({
                "message": f"There is no such gsc",
                "status": "failed"
            })

@gscs_api_blueprint.route('/activate/<id>', methods=['POST'])
def activate(id):
    gsc = Gsc.get_or_none(Gsc.id == id)

    if gsc:
        gsc.is_activated = True
        gsc.is_active = True
        if gsc.save(only=[Gsc.is_activated, Gsc.is_active]):
            return jsonify({
                "message": f"Successfully activated {gsc.name} as a gsc",
                "status": "success"
            })
        else:
            return jsonify({
                "message": f"Failed to activate {gsc.name} as a gsc",
                "status": "failed"
            })
    else:
        return jsonify({
                "message": f"There is no such gsc",
                "status": "failed"
            })