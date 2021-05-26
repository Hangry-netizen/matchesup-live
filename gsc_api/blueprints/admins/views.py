from flask import Blueprint, jsonify,request
from models.admin import Admin
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token

admins_api_blueprint = Blueprint('admins_api',
                             __name__)

@admins_api_blueprint.route('/', methods=['GET'])
def index():
    admins = Admin.select()
    return jsonify([{
        "username": admin.username,
        "id": admin.id
        } for admin in admins])

@admins_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    admin_id = get_jwt_identity()
    admin = Admin.get_or_none(Admin.id == admin_id)
    if admin:
        return jsonify({
            "id": admin.id,
            "username": admin.username
        })


@admins_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    if username and password:
        admin = Admin(
            username = username,
            password = password
        )
        if admin.save():
            token = create_access_token(identity=admin.id)
            return jsonify({
                "auth_token": token,
                "message": "Successfully created an admin and signed in",
                "status": "success",
                "admin": {
                    "id": admin.id,
                    "name": admin.username
                }
            })
        elif admin.errors != 0:
            return jsonify({
                "message": [error for error in admin.errors],
                "status": "failed"
            })
    else:
        return jsonify({
            "message": "All fields are required!",
            "status": "failed"
        })
