from Database.migrations import db
from flask import json

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(50), nullable=False)
    processed = db.Column(db.Boolean, nullable=False)


    def __repr__(self):
        image = { 'id': self.id, 'image_name': self.image_name, 'processed': self.processed }
        image = json.dumps(image)
        return image
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}