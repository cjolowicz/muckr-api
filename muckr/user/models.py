'''User models.'''
import secrets
from datetime import datetime, timedelta

from marshmallow import Schema, fields
from marshmallow.validate import Length

from muckr.extensions import bcrypt
from muckr.extensions import database as db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(64), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        data = bcrypt.generate_password_hash(password)
        self.password_hash = data.decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(32)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        if self.token is not None:
            self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is not None and user.token_expiration is not None and \
                user.token_expiration > datetime.utcnow():
            return user


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True, validate=Length(min=1))
    email = fields.Email(required=True)
    password = fields.Function(load_only=True, required=True)

    class Meta:
        strict = True
