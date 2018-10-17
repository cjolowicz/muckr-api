from marshmallow import Schema, fields, post_load

from muckr.extensions import bcrypt
from muckr.extensions import database as db


def generate_password_hash(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class UserSchema(Schema):
    __model__ = User

    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password_hash = fields.Function(load_only=True,
                                    load_from='password',
                                    deserialize=generate_password_hash)

    @post_load
    def make_object(self, data):
        return self.__model__(**data)
