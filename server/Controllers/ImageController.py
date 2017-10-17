import os
from flask import jsonify, send_from_directory
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException, NotFound
import uuid

from Database.initialize import db
from Models.Cropped import Cropped
from Models.Image import Image
from Controllers import JudgeController

app = db.app

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
orientations = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_raw_image():
    try:
        image = Image.query.filter_by(processed=False).first()
        if image is None:
            return "No new images", 204
        image.processed = True
        db.session.commit()
        return jsonify(image.as_dict()), 200
    except SQLAlchemyError as error:
        print(error)
        return "Exception when retrieving image, check logs", 400
    except NotFound as error:
        return "Unable to find image.", 404
    except Exception as error:
        print(error)
        return "Unknown issue. Check logs", 400


def get_image_by_id(id):
    try:
        image = Image.query.filter_by(id=id).first()
        if image is None:
            return "Unable to find image by id: %d" % id, 404
        image.processed = True
        db.session.commit()
        root_dir = os.path.dirname(os.getcwd())
        return send_from_directory(os.path.join(root_dir, 'server', 'images'), image.image_name)
    except SQLAlchemyError as error:
        print(error)
        return "Exception when retrieving image, check logs", 400
    except NotFound as error:
        print(error)
        return "Unable to find image.", 404
    except Exception as error:
        print(error)
        return "Unknown issue. Check logs", 400


def post_raw_image(request):
    try:
        if 'image' not in request.files:
            return 'No image was included in request', 400
        f = request.files['image']
        if f.filename == '':
            return 'File name was invalid', 400
        if f and __allowed_file(f.filename):
            filename = str(uuid.uuid4().hex) + ".jpeg"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = Image(image_name=filename, processed=False)
            db.session.add(image)
            db.session.commit()
            return 'Successfully uploaded the image'
        return 'File is invalid or invalid file type', 400
    except SQLAlchemyError as error:
        print(error)
        return 'Exception while saving image', 400
    except Exception as error:
        print(error)
        return "Unknown issue. Check logs", 400


def post_processed_image(request, token):
    try:
        if 'image' not in request.files:
            return 'No image was included in request', 400
        if 'original_id' not in request.form:
            return 'Missing original_id', 400
        data = request.form
        if(data is None):
            return 'Request was empty', 400
        if data['orientation'] not in orientations:
            return "Unknown orientation " + data['orientation'] + "; known orientations ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']", 400
        f = request.files['image']
        if f.filename == '':
            return 'File name was invalid', 400
        if f and __allowed_file(f.filename):
            filename = str(uuid.uuid4().hex) + ".jpeg"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #process lat/long here
            if data['has_odlc'] == '1':
                cropped = Cropped(image_name=filename, has_odlc=1, shape=data['shape'], 
                                background_color=data['background_color'], alphanumeric=data['alphanumeric'], alphanumeric_color=data['alphanumeric_color'], 
                                orientation=data['orientation'], original_id=data['original_id'])
                db.session.add(cropped)
                code = JudgeController.post_odlc(token, cropped)
                if code == 201:
                    return "Successfully submitted picture to judging server.", 201
                if code == 403:
                    return "Judging server token is expired. Reauthenticate", 401
                else:
                    return "Issue submitting picture for judging, check logs", 400

            else:
                cropped = Cropped(image_name=filename, has_odlc=0, original_id=data['original_id'])
                db.session.add(cropped)
            db.session.commit()  
            return 'Successfully uploaded the image'
        return 'File is invalid or invalid file type', 400
    except SQLAlchemyError as error:
        print(error)
        return 'Exception while saving image', 400
    except HTTPException as error:
        print(error)
        return 'Missing paramter', 400
    except Exception as error:
        print(error)
        return "Unknown issue. Check logs", 400


def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS