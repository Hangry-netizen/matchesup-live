from flask import Blueprint, jsonify, request
from models.admin import Admin
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

sessions_api_blueprint = Blueprint('sessions_api',
                             __name__)

@sessions_api_blueprint.route('/login/admin', methods=['POST'])
def login_admin():
    data = request.json

    admin = Admin.get_or_none(username=data.get('username'))
    
    if admin:
        hash_password = admin.password_hash
        result = check_password_hash(hash_password, data.get('password'))

        if result:
            token = create_access_token(identity=admin.id)
            return jsonify({"auth_token": token, 'id': admin.id, 'username': admin.username})

    return jsonify({"Error": "Invalid credentials"})