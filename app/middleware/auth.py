from functools import wraps
from datetime import datetime, timezone
from app import response
from app.model.user import Token
from flask import request

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return response.notAuthorized([], 'Failed authenticating. Token is missing!')
            
            parts = auth_header.split()
            if parts[0].lower() != 'bearer' or len(parts) != 2:
                return response.notAuthorized([], 'Failed authenticating. Invalid token header format. Expected "Bearer <token>"')

            token = parts[1]

            token_data = Token.query.filter_by(token=token).first()

            if not token_data:
                return response.notAuthorized([], 'Failed authenticating. Token is invalid.')

            expires_at = token_data.expires_at
            expires_at = expires_at.replace(tzinfo=timezone.utc)

            if not token_data or expires_at < datetime.now(timezone.utc):
                return response.notAuthorized([], 'Failed authenticating. Token is expired')

            # Menambahkan data ke kwargs berdasarkan kebutuhan fungsi asli
            if 'token' in f.__code__.co_varnames:
                kwargs['token'] = token
            if 'current_user' in f.__code__.co_varnames:
                kwargs['current_user'] = token_data.user

            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return response.serverError([], 'Failed authenticating. Internal server error.')
    return decorated

