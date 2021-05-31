from flask import Blueprint, jsonify, request
from models.gsc import *
from helpers import send_gsc_consent_email
from helpers import send_approved_email

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
        "ff_name": gsc.ff_name,
        "ff_email": gsc.ff_email
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
                ff_email = ff_email
        )
        if gsc.save():
            email = gsc.email
            data = {
                "gscf_name": gsc.name,
                "ff_name": gsc.ff_name,
                "ff_email": gsc.ff_email,
                "consent_url": f"www.matchesup.com/good-single-christian-friend/{gsc.uuid}/consent",
                "gsc_profile_link": f"www.matchesup.com/good-single-christian-friend/{gsc.uuid}"
            }

            send_email = send_gsc_consent_email(to_email=email, dynamic_template_data=data)

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
        "ff_name": gsc.ff_name,
        "ff_email": gsc.ff_email
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
    is_active = data.get('is_active') 

    if (
    is_approved or 
    is_active):
        approve_gsc.is_approved = is_approved 
        approve_gsc.is_active = is_active 

        if approve_gsc.save(only=[
            Gsc.is_approved, 
            Gsc.is_active,
            ]):

            email = approve_gsc.email
            data = {
                "gscf_name": approve_gsc.name,
                "edit_url": f"www.matchesup.com/good-single-christian-friend/{approve_gsc.uuid}"
            }

            send_email = send_approved_email(to_email=email, dynamic_template_data=data)

            return jsonify({
                "message": "Successfully updated GSCF status!",
                "status": "success",
                "gsc": {
                    "uuid": approve_gsc.uuid,
                    "name": approve_gsc.name,
                    "is_approved": approve_gsc.is_approved,
                    "is_active": approve_gsc.is_active
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

    if (
    is_approved != "" or 
    is_active != ""):
        status.is_approved = is_approved 
        status.is_active = is_active 

        if status.save(only=[
            Gsc.is_approved, 
            Gsc.is_active,
            ]):

            return jsonify({
                "message": "Successfully updated GSCF status!",
                "status": "success",
                 "gsc": {
                    "uuid": status.uuid,
                    "name": status.name,
                    "is_approved": status.is_approved,
                    "is_active": status.is_active
                 }
            })

        elif status.errors != 0:
            return jsonify({
                "message": [error for error in approve.errors],
                "status": "failed"
            })
    
    else:
        return jsonify({
            "message": "At least on field must be filled",
            "status": "failed"
        })

@gscs_api_blueprint.route('/superadmin/edit/<uuid>', methods=['POST'])
def superadmin_edit(uuid):
    update_gsc = Gsc.get_or_none(Gsc.uuid == uuid)

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
    consent = data.get('consent')
    social_media_profile_link = data.get('social_media_profile_link') 
    preferred_contact_method = data.get('preferred_contact_method') 
    contact_info = data.get('contact_info') 
    notification_frequency = data.get('notification_frequency')
    what_is_important_to_me = data.get('what_is_important_to_me') 
    is_approved = data.get('is_approved') 
    is_active = data.get('is_active') 

    if (
    name != "" or 
    email != "" or
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
        update_gsc.email = email
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

        if update_gsc.save():
            return jsonify({
                "message": f"Successfully updated {update_gsc.name}'s profile!",
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