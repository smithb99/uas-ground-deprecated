import os
from flask import Flask, url_for, request, send_from_directory, json, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException, NotFound
from Database.migrations import db
from Models.Cropped import Cropped
from Models.Image import Image
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
import uuid



UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = db.app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# GET /api/image
@app.route('/api/image')
def api_get_image():
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


# GET /api/image/<int:id>
@app.route('/api/image/<int:id>')
def api_get_image_by_id(id):
    try:
        image = Image.query.filter_by(id=id).first()
        if image is None:
            return "Unable to find image by id: %d" % id, 404
        image.processed = True
        db.session.commit()
        print(image.image_name)
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



# POST /api/image
@app.route('/api/image', methods = { 'POST' })
def api_post_raw_image():
    try:
        if 'image' not in request.files:
            return 'No image was included in request', 400
        f = request.files['image']
        if f.filename == '':
            return 'File name was invalid', 400
        if f and allowed_file(f.filename):
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


@app.route('/api/image/cropped', methods = { 'POST' })
def api_post_processed_image():
    try:
        if 'image' not in request.files:
            return 'No image was included in request', 400
        if 'original_id' not in request.form:
            return 'Missing original_id', 400
        data = request.form
        if(data is None):
            return 'Request was empty', 400
        #todo capture confirmed correctly
        f = request.files['image']
        if f.filename == '':
            return 'File name was invalid', 400
        if f and allowed_file(f.filename):
            filename = secure_filename(str(uuid.uuid4().hex) + ".jpeg")
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #process lat/long here
            cropped = Cropped(image_name=filename, has_odlc=data['has_odlc'], shape=data['shape'], 
                            background_color=data['background_color'], alphanumeric=data['alphanumeric'], alphanumeric_color=data['alphanumeric_color'], 
                            orientation=data['orientation'], original_id=data['original_id'])
            db.session.add(cropped)
            db.session.commit()
            #todo: submit image for judging
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


#return jsonify(image.as_dict()), 200



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
