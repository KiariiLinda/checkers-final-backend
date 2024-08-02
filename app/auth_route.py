from flask import Blueprint,jsonify,request # type: ignore
from flask_jwt_extended import create_access_token,JWTManager # type: ignore
from . import db, bcrypt
from datetime import timedelta,datetime
from .models import Users, Games
import json


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    body=request.get_json()
    username=body.get('username')
    email=body.get('email')
    password=body.get('password')
        
    ## Validation
    if not email or not password or not username:
        return jsonify({'message':"Required field missing"}),400
        
    if len(email)<4:
        return jsonify({'message':"Email too short"}),400
        
    if len(username)<3:
        return jsonify({'message':"Username too short"}),400
        
    if len(password)<6:
        return jsonify({'message':"Password too short. Use a stronger password!"}),400
        
    existing_member=Users.query.filter_by(email=email).first()

    if existing_member:
        return jsonify({'message':f"The email {email} is already in use."}),400
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    users = Users(username=username, email=email, password=hashed_password)
    db.session.add(users)
    db.session.commit()
    return jsonify({'message':"Sign up successful!"}),201

@auth_blueprint.route("/signin", methods=["POST"])
def signin():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')

    ## Validation
    if not email or not password:
        return jsonify({'message': "Required field missing"}), 400

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': "User not found"}), 400
        
    pass_ok = bcrypt.check_password_hash(user.password, password)



    # ACCESS TOKEN
    expires = timedelta(hours=24)
    access_token = create_access_token(identity=user.details(), expires_delta=expires)
    if not pass_ok:
            return jsonify({'message': "Invalid password"}), 401
        
    # Return user details directly
    return jsonify({'user':user.details(),'token':access_token})