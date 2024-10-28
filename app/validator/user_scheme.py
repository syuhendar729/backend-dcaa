from app import ma  
from marshmallow import fields, validate 

# Validator khusus untuk memeriksa tipe file berdasarkan ekstensi
def file_type_validator(file):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    if file:
        file_extension = file.filename.rsplit('.', 1)[-1].lower()
        if file_extension not in allowed_extensions:
            raise ValidationError("Invalid file type. Only PNG, JPG, or JPEG files are allowed.")

class RegisterUserScheme(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True, validate=validate.Email(error="Invalid email address."))
    password = fields.String(required=True, validate=validate.Length(min=6), error_messages={"required": "Password is required."})
    profile_picture = fields.Field(validate=file_type_validator)
    #  profile_picture = fields.String(validate=validate.URL(error="invalid url"))

class UpdateUserScheme(ma.Schema):
    username = fields.String(required=False, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=False, validate=validate.Email(error="Invalid email address."))
    profile_picture = fields.Field(validate=file_type_validator)
    #  profile_picture = fields.String(validate=validate.URL(error="invalid url"))
    #  password = fields.String(required=False, validate=validate.Length(min=6), error_messages={"required": "Password is required."})

class LoginUserScheme(ma.Schema):
    email = fields.Email(required=True, validate=validate.Email(error="Invalid email address."))
    password = fields.String(required=True, validate=validate.Length(min=6), error_messages={"required": "Password is required."})

class ResetPasswordScheme(ma.Schema):
    old_password = fields.String(required=True, validate=validate.Length(min=6), error_messages={"required": "Old Password is required."})
    new_password = fields.String(required=True, validate=validate.Length(min=6), error_messages={"required": "New Password is required."})

