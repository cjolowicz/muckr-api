from marshmallow import Schema, fields

from muckr.extensions import bcrypt
from muckr.extensions import database as db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        data = bcrypt.generate_password_hash(password)
        self.password_hash = data.decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class UserSchema(Schema):
    __model__ = User

    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Function(load_only=True, required=True)
