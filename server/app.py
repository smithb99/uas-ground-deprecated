import os
from flask import Flask, url_for, request, send_from_directory, json, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException, NotFound
from migrations import db, Image
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound



UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = db.app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# GET /api/image
@app.route('/api/image')
def api_gui(id=None):
    try:
        image = Image.query.filter_by(processed=False).first()
        if image is None:
            return "No new images", 204
        image.processed = True
        db.session.commit()
        return send_from_directory(directory='images', filename=image.image_name)
    except SQLAlchemyError as error:
        print(error)
        return "Exception when retrieving image, check logs", 400
    except NotFound as error:
        return "Unable to find image.", 404
    except Exception as error:
        print(error)
        return "Unknown issue. Check logs", 400


# POST /api/image
@app.route('/api/image', methods = { 'POST' })
def api_image():
    try:
        if 'image' not in request.files:
            return 'No image was included in request', 400
        file = request.files['image']
        if file.filename == '':
            return 'File name was invalid', 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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


#return jsonify(image.as_dict()), 200



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
