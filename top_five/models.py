from top_five import app, db, login

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'An account has been created! Your username is {self.username} and your account email is {self.email}.'

class AvengerInformation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(200),nullable=False,unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, name, email, phone_number, user_id):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.user_id = user_id

    def __repr__(self):
        return f'{name}\'s phone number is {phone_number}.'

