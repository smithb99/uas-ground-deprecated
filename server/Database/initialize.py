from flask_sqlalchemy import SQLAlchemy
from flask import Flask
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