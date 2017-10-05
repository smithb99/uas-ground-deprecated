import os
from flask import Flask, url_for, request, send_from_directory, json
from werkzeug.utils import secure_filename
from migrations import db



UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# GET /api/gui
@app.route('/api/gui')
def api_gui():
    try:
        #conn = mysql.connect()
        #cursor = conn.cursor()
        #cursor.execute("SELECT * FROM images WHERE processed = 0 LIMIT 1")
        #data = cursor.fetchone()
        #if data is None:
        #    return "", 204
        #if data[1]:
        #    cursor.execute("UPDATE images SET processed = 1 WHERE id = %s", data[0])
        #    conn.commit()
        #    return send_from_directory(directory='images', filename=data[1])
        return "Image name was invalid", 400
    except:
        return "Exception when retrieving image, check logs", 400


# POST /api/image
@app.route('/api/image', methods = { 'POST' })
def api_image():
    try:
        #if 'image' not in request.files:
        #    return 'No image was included in request', 400
        #file = request.files['image']
        #if file.filename == '':
        #    return 'File name was invalid', 400
        #if file and allowed_file(file.filename):
        #    filename = secure_filename(file.filename)
        #    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #    conn = mysql.connect()
        #    cursor = conn.cursor()
        #    cursor.execute("INSERT INTO images (image_name) values (%s) ", filename)
        #    data = cursor.fetchall()
        #    if len(data) is 0:
        #        conn.commit()
        #        return 'Successfully uploaded the image'
        #    return 'Unable to save image in database', 400
        return 'File is invalid or invalid file type', 400
    except:
        return 'Exception while saving image', 400





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
