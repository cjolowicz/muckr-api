"""Artist model."""
from marshmallow import Schema, fields
from marshmallow.validate import Length

from muckr.extensions import database as db


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return "<Artist {}>".format(self.name)


class ArtistSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=Length(min=1, max=128))
