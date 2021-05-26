from flask import Blueprint, jsonify, request
from models.single_communities import *

single_communities_api_blueprint = Blueprint('single_communities_api',
                             __name__)

@single_communities_api_blueprint.route('/', methods=['GET'])
def index():
  singles = SingleCommunities.select()
  return jsonify([{
      "id": single.id,
      "email": single.email
      }
      for single in singles
    ])
    
@single_communities_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json

    email = data.get('email')

    if email:
      single = SingleCommunities(
        email = email,
      )

      if single.save():
        return jsonify({
            "message": "Successfully added email to single communities",
            "status": "success",
            "single_communities": 
            {
                "id": single.id,
                "email": single.email
            }
        })
      else:
        return jsonify({
            "message": "All fields are required!",
            "status": "failed"
        })