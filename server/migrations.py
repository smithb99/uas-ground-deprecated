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


db = SQLAlchemy(app)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(20), nullable=False)
    confirmed = db.Column(db.Boolean)
    shape = db.Column(db.String(20))
    shape_color = db.Column(db.String(20))
    letter = db.Column(db.CHAR)
    letter_color = db.Column(db.String(20))
    orientation = db.Column(db.String(20))
    processed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        image = { 'image_name': self.image_name, 'confirmed': self.confirmed, 'shape': self.shape, 
            'shape_color': self.shape_color, 'letter': self.letter, 'letter_color': self.letter_color,
            'orientation': self.orientation, 'processed': self.processed }
        image = json.dumps(image)
        return image
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
