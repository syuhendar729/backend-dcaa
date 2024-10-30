from app.model.user import User, Token
from app import response, db
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, timezone
from config import Config
import os
import secrets


def get_all_user():
    try:
        user = User.query.all()
        data = formatarray(user)
        print(f'get_all_user: {data}')
        return response.success(data, 'Success get all users.')
    except Exception as e:
        print(e)

def get_detail_user(current_user):
    try:
        data = singleObject(current_user)
        print(data)
        return response.success(data, 'Success get detail user.')
    except Exception as e:
        print(e)
        return response.serverError(f'{e}', 'Failed get user. Internal Server Error.')

def create_user():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        profile_picture = request.form.get('profile_picture')
        
        username_exists = User.query.filter_by(username = username).first()
        email_exists = User.query.filter_by(email = email).first()

        if username_exists:
            return response.badRequest([], 'Failed create user. Username already exists.')
        if email_exists:
            return response.badRequest([], 'Failed create user. Email already exists.')

        user = User(
                username = username, 
                email= email,
                profile_picture= profile_picture
        )

        user.set_password(password)
        print(user)
        db.session.add(user)
        db.session.commit()

        return response.success( { email: email, username: username }, 'Success create user data.')
    except Exception as e:
        print(e)
        return response.serverError(f'{e}', 'Failed create user. Internal Server Error.')

def update_user(id):
    try:
        file_url = None
        username = request.form.get('username')
        email = request.form.get('email')

        username_exists = User.query.filter_by(username = username).first()
        email_exists = User.query.filter_by(email = email).first()
        user = User.query.filter_by(id=id).first()
        if username_exists and user.username != username:
            return response.badRequest([], 'Failed update user. Username already exists.')
        if email_exists and user.email != email:
            return response.badRequest([], 'Failed update user. Email already exists.')
        

        if 'username' in request.form:
            user.username = username

        if 'email' in request.form:
            user.email = email

        if 'profile_picture'in request.files:
            try:
                file_url = upload_image(request.files['profile_picture'])
                user.profile_picture = file_url
            except Exception as e:
                print(e)
                return response.badRequest([], str(e))  


        input = {
            'username': username,
            'email': email,
            'profile_picture': file_url
        }
        db.session.commit()

        return response.success(input, 'Success update user data.')
    except Exception as e:
        print(e)
        return response.serverError(f'{e}', 'Failed update user. Internal Server Error.')

def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'Failed delete user. User not found.')
        
        db.session.delete(user)
        db.session.commit()

        return response.success(id, 'Success delete user.')
    except Exception as e:
        print(e)
        return response.serverError(f'{e}', 'Failed delete user. Internal Server Error.')

def login_user():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            return response.badRequest([], 'Failed login. User not registered.')
        if not user.check_password(password):
            return response.badRequest([], 'Failed login. Wrong password.')

        data = singleObject(user)

        access_token = generate_token(user.id)

        return response.success({
            "data" : data,
            "access_token" : access_token,
        }, "Success login!")
    except Exception as e:
        print(e)
        return response.serverError(f'{e}', 'Failed login user. Internal Server Error.')

def logout_user(token):
    try:
        token = Token.query.filter_by(token=token).first()
        db.session.delete(token)
        db.session.commit()
        return response.success([], 'Success logout user.')
    except Exception as e:
        print(e)
        return response.serverError(f'{e}', 'Failed logout user. Internal Server Error.')


def reset_password(id):
    try:
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        user = User.query.filter_by(id=id).first()
        if not user.check_password(old_password):
            return response.badRequest([], 'Failed update password. Wrong old password.')
        if old_password == new_password:
            return response.badRequest([], "Failed update password. Can't same old and new password.")
        user.set_password(new_password)
        db.session.commit()
        return response.success([], 'Success update password.')
    except Exception as e:
        print(e)
        return response.serverError(f'{e}', 'Failed update password. Internal server error.')

def get_url_image(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user.profile_picture is None:
            url_image = 'null'
        else:
            url_image = f'{Config.URL_HOST}{user.profile_picture}'
        return response.success({ 'url_image': url_image }, 'Success get url profile image.')
    except Exception as e:
        print(e)
        return response.serverError([], 'Failed get url image. Internal server error.')


        

# =========================================== HELPER ===========================================
def generate_token(user_id):
    token = secrets.token_hex(32)  # Membuat token 64 karakter unik
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)  # Token berlaku selama 1 jam
    new_token = Token(user_id=user_id, token=token, expires_at=expires_at)
    db.session.add(new_token)
    db.session.commit()
    return token

def upload_image(file):
    filename = secure_filename(file.filename)
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        filepath = os.path.join(Config.STATIC_FOLDER, filename)
        file.save(filepath)  # Simpan file di folder static Flask

        file_url = f"/static/{filename}"
        return file_url
    else:
        raise Exception("Invalid file type. Only PNG, JPG, or JPEG files are allowed.")



def formatarray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))
    
    return array

def singleObject(data):
    data = {
        'id' : data.id,
        'username' : data.username,
        'email' : data.email,
        'profile_picture' : data.profile_picture,
    }
    return data
