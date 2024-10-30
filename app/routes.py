from sqlalchemy.sql.functions import current_user
from app import app, response
from app.controller import UserController
from app.validator.user_scheme import RegisterUserScheme, ResetPasswordScheme, UpdateUserScheme, LoginUserScheme
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.validator.user_scheme import RegisterUserScheme, UpdateUserScheme, LoginUserScheme
from marshmallow import ValidationError 
from app.middleware.auth import token_required

@app.route('/')
def index():
    return response.success([], 'Welcome to Entry Task DCAA.')

@app.route('/users', methods=['GET'])
def show_users():
    return UserController.get_all_user()

@app.route('/user', methods=['POST'])
def create_user():
    data = request.form.to_dict()
    try:
        print(data)
        RegisterUserScheme().load(data)
    except ValidationError as err:
        return response.badRequest(err.messages, 'Validation failed.')
    return UserController.create_user()

@app.route('/user', methods=['GET'])
@token_required
def get_detail_user(current_user):
    print(current_user)
    return UserController.get_detail_user(current_user)

@app.route('/user', methods=['PATCH'])
@token_required
def update_user(current_user):
    data = request.form.to_dict()
    try:
        UpdateUserScheme().load(data)
    except ValidationError as err:
        print(err)
        return response.badRequest(err.messages, 'Validation failed.')
    return UserController.update_user(current_user.id)


@app.route('/user', methods=['DELETE'])
@token_required
def delete_user(current_user):
    return UserController.delete_user(current_user.id)

@app.route('/login', methods=['POST'])
def login_user():
    data = request.form.to_dict()
    try:
        LoginUserScheme().load(data)
    except ValidationError as err:
        print(err)
        return response.badRequest(err.messages, 'Validation failed.')
    return UserController.login_user()

@app.route('/logout', methods=['POST'])
@token_required
def logout_user(token):
    return UserController.logout_user(token)

@app.route('/reset-password', methods=['PUT'])
@token_required
def reset_password(current_user):
    data = request.form.to_dict()
    try:
        ResetPasswordScheme().load(data)
    except ValidationError as err:
        print(err)
        return response.badRequest(err.messages, 'Validation failed.')
    return UserController.reset_password(current_user.id)


@app.route('/get-profile', methods=['GET'])
@token_required
def get_url_image(current_user):
    return UserController.get_url_image(current_user.id)





