from flask import Blueprint, jsonify, request
from models.hello import Hello
from models.gsc import Gsc
from helpers import sendgrid

hellos_api_blueprint = Blueprint('hellos_api',
                             __name__)

@hellos_api_blueprint.route('/', methods=['GET'])
def index():
    hellos = Hello.select()

    response = []

    for hello in hellos:

        said_hi = hello.said_hi
        hi_recipient = hello.hi_recipient

        data = {
            "hello_id": hello.id,
            "said_hi": said_hi.name,
            "hi_recipient": hi_recipient.name,
            "hi_recipient": hi_recipient.notification_frequency
        }
        
        response.append(data)

    return jsonify(response)


@hellos_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json

    said_hi = data.get("said_hi")
    hi_recipient = data.get("hi_recipient")

    if said_hi and hi_recipient:
        hello = Hello(
                said_hi = said_hi,
                hi_recipient = hi_recipient
        )
        if hello.save():
            hi_recipient = hello.hi_recipient
            said_hi = hello.said_hi
            
            monthly_hellos = said_hi.monthly_hellos - 1
            said_hi.monthly_hellos = monthly_hellos
    
            if said_hi.save(only=[Gsc.monthly_hellos]):
                if hi_recipient.notification_frequency == "same_day":
                    gsc_email = hi_recipient.email
                    ff_email = hi_recipient.ff_email
                    hello_notification_for_gsc_template_id = "d-50854c382f034a1cba98fa13af5e7df9"
                    hello_notification_for_ff_template_id = "d-6a73fe538bef4c779114ab44477d5d37"
                    data = {
                        "gscf_name": hi_recipient.name,
                        "ff_name": hi_recipient.ff_name,
                        "hello_page_url": f"www.matchesup.com/good-single-christian-friend/{hi_recipient.uuid}/hellos"
                    }
                    
                    send_email_to_gsc = sendgrid(to_email=gsc_email, dynamic_template_data=data, template_id=hello_notification_for_gsc_template_id)
                    send_email_to_ff = sendgrid(to_email=ff_email, dynamic_template_data=data, template_id=hello_notification_for_ff_template_id)
    
                    return jsonify({
                        "message": f"You've said hi to {hi_recipient.name}!",
                        "status": "success",
                        "msg": "Successfully emailed hi recipient"
                    })
    
                return jsonify({
                    "message": f"You've said hi to {hi_recipient.name}!",
                    "status": "success"
                })
            else:
                return jsonify({
                    "message": "Failed to set monthly hello limit",
                    "status": "failed"
                })
        elif hello.errors != 0:
            return jsonify({
                "message": [error for error in reference.errors],
                "status": "failed"
            })

@hellos_api_blueprint.route('/contacted/<id>', methods=['POST'])
def update(id):
    hello = Hello.get_or_none(Hello.id == id)
    data = request.json

    contacted = data.get('contacted')

    if contacted:
        hello.contacted = contacted
        
        if hello.save(only=[Hello.contacted]):
            return jsonify({
                "message": f"Successfully updated contacted status!",
                "status": "success"
            })
        
        elif hello.errors != 0:
            return jsonify({
                "message": [error for error in reference.errors],
                "status": "failed"
            })

@hellos_api_blueprint.route('/remove/<id>', methods=['POST'])
def remove(id):
    hello = Hello.get_or_none(Hello.id == id)
    data = request.json

    removed = data.get('removed')

    if removed:
        hello.removed=removed
        
        if hello.save(only=[Hello.removed]):
            return jsonify({
                "message": f"Successfully removed 'say hi'!",
                "status": "success"
            })
        
        elif hello.errors != 0:
            return jsonify({
                "message": [error for error in reference.errors],
                "status": "failed"
            })

@hellos_api_blueprint.route('/delete/<id>', methods=['POST'])
def delete(id):
    hello = Hello.get_or_none(Hello.id == id)

    if hello:
        if hello.delete_instance():
            return jsonify({
                "message": "Successfully deleted hello",
                "status": "success"
            })
        else:
            return jsonify({
                "message": "Failed to delete hello",
                "status": "failed"
            })

@hellos_api_blueprint.route('/send-notification/<id>', methods=['POST'])
def notification(id):
    hello = Hello.get_or_none(Hello.id == id)

    if hello:
        hi_recipient = hello.hi_recipient
        if hi_recipient.notification_frequency == "weekly":
                    gsc_email = hi_recipient.email
                    ff_email = hi_recipient.ff_email
                    hello_notification_for_gsc_template_id = "d-50854c382f034a1cba98fa13af5e7df9"
                    hello_notification_for_ff_template_id = "d-6a73fe538bef4c779114ab44477d5d37"
                    data = {
                        "gscf_name": hi_recipient.name,
                        "ff_name": hi_recipient.ff_name,
                        "hello_page_url": f"www.matchesup.com/good-single-christian-friend/{hi_recipient.uuid}/hellos"
                    }
                    
                    send_email_to_gsc = sendgrid(to_email=gsc_email, dynamic_template_data=data, template_id=hello_notification_for_gsc_template_id)
                    send_email_to_ff = sendgrid(to_email=ff_email, dynamic_template_data=data, template_id=hello_notification_for_ff_template_id)
    
                    return jsonify({
                        "message": f"Successfully sent hello notification to {hi_recipient.name}!",
                        "status": "success"
                    })