from flask import Blueprint, jsonify, request
from models.hello import Hello
from models.gsc import Gsc

hellos_api_blueprint = Blueprint('hellos_api',
                             __name__)
    
@hellos_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json

    said_hi = data.get("said_hi")
    hi_recipient = data.get("hi_recipient")

    hello = Hello(
            said_hi = said_hi,
            hi_recipient = hi_recipient
        )
    if hello.save():
        hi_recipient = hello.hi_recipient
        
        return jsonify({
            "message": f"You've said hi to {hi_recipient.name}!",
            "status": "success"
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