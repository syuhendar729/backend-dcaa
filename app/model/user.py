from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Hash password untuk keamanan
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Cek password saat login
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Fungsi untuk representasi user sebagai string
    def __repr__(self):
        return f'<User {self.username}>'