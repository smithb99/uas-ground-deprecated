from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy

import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

username = cfg['mysql']['user']
password = cfg['mysql']['password']
database = cfg['mysql']['db']
host = cfg['mysql']['host']
port = cfg['mysql']['port']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + username +':' + password + '@' + host + ':' + port + '/' + database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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