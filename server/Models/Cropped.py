from Database.initialize import db
from Models.Image import Image
from flask import json

class Cropped(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(50), nullable=False)
    has_odlc = db.Column(db.Boolean, nullable=False)
    shape = db.Column(db.String(20))
    background_color = db.Column(db.String(20))
    alphanumeric = db.Column(db.CHAR)
    alphanumeric_color = db.Column(db.String(20))
    orientation = db.Column(db.String(20))
    latitude = db.Column(db.FLOAT)
    longitude = db.Column(db.FLOAT)

    original_id = db.Column(db.Integer, db.ForeignKey(Image.id), index=True, nullable=False)
    original = db.relationship(Image, backref=db.backref('original_image', remote_side=Image.id))

    def __repr__(self):
        cropped = { 'id': self.id, 'image_name': self.image_name, 'has_odlc': self.has_odlc, 'shape': self.shape, 
            'background_color': self.background_color, 'alphanumeric': self.alphanumeric, 'alphanumeric_color': self.alphanumeric_color,
            'orientation': self.orientation, 'latitude': self.latitude, 'longitude': self.longitude }
        cropped = json.dumps(cropped)
        return cropped

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}