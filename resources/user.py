from flask_restplus import Resource, Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, jwt_refresh_token_required, create_refresh_token
)
from db import db
from models.user import User
from werkzeug.security import safe_str_cmp

api = Api()


class UserRegister(Resource):
    def post(self):
        if len(api.payload['username']) < 6 and len(api.payload['password']) < 6:
            return {"msg": "Password or username too short!"}, 400
        all_users = [user for user in User.query.all()]
        for user in all_users:
            if user.name == api.payload['username']:
                return {'msg': 'User already exists!'}, 401
        new_user = User(
            name=api.payload['username'], password=api.payload['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'msg': 'New user added'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}, 200


class UserLogin(Resource):
    def post(self):
        username = api.payload['username']
        password = api.payload['password']
        if not username or not password:
            return {"msg": "Username and password can't be left blank!"}, 400
        user = User.find_by_username(username)
        if not user:
            return {"msg": "No user found with such username"}, 401
        if safe_str_cmp(password, user.password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {"msg": "Password inccorect!"}, 401

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        return {'logged': User.find_by_id(user_id).name}


class Users(Resource):
    @jwt_required
    def get(self):
        one_user = User.query.all()
        return {'users': [user.json() for user in User.query.all()]}
