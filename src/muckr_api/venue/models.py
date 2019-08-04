"""Venue model."""
from marshmallow import Schema, fields
from marshmallow.validate import Length

from muckr_api.extensions import database as db


class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    city = db.Column(db.String(128))
    country = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return "<Venue {}>".format(self.name)


class VenueSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=Length(min=1, max=128))
    city = fields.Str(required=True, validate=Length(min=1, max=128))
    country = fields.Str(required=True, validate=Length(min=1, max=128))
