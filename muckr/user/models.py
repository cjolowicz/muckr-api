from marshmallow import Schema, fields

import muckr.extensions
from muckr.extensions import database as db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = muckr.extensions.bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return muckr.extensions.bcrypt.check_password_hash(
            self.password_hash, password)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    password_hash = fields.Str(load_only=True)
