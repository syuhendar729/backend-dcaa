from sqlalchemy.sql.functions import current_user
from app import app, response
from app.controller import UserController
from app.validator.user_scheme import RegisterUserScheme, ResetPasswordScheme, UpdateUserScheme, LoginUserScheme
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.validator.user_scheme import RegisterUserScheme, UpdateUserScheme, LoginUserScheme
from marshmallow import ValidationError 

@app.route('/')
def index():
    return response.success([], 'Welcome to Entry Task DCAA.')

@app.route('/users', methods=['GET'])
@jwt_required()
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
@jwt_required()
def show_user_byid():
    current_user = get_jwt_identity()
    print(current_user)
    return UserController.get_detail_user(current_user.get('id'))

@app.route('/user', methods=['PATCH'])
@jwt_required()
def update_user():
    current_user = get_jwt_identity()
    data = request.form.to_dict()
    try:
        UpdateUserScheme().load(data)
    except ValidationError as err:
        print(err)
        return response.badRequest(err.messages, 'Validation failed.')
    return UserController.update_user(current_user.get('id'))

@app.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user = get_jwt_identity()
    return UserController.delete_user(current_user.get('id'))

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
@jwt_required()
def logout_user():
    return UserController.logout_user()

@app.route('/reset-password', methods=['PUT'])
@jwt_required()
def reset_password():
    data = request.form.to_dict()
    current_user = get_jwt_identity()
    try:
        ResetPasswordScheme().load(data)
    except ValidationError as err:
        print(err)
        return response.badRequest(err.messages, 'Validation failed.')
    return UserController.reset_password(current_user.get('id'))


@app.route('/protect', methods=['GET'])
@jwt_required()
def protect():
    current_user = get_jwt_identity()
    return response.success(current_user, 'Success user authorized.')
