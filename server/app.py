from flask import Flask, url_for, request, send_from_directory
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/api/gui')
def api_gui():
    filename = request.args.get('filename')
    #todo: remove filename from db
    return send_from_directory(directory='images', filename=filename)
    return 'GUI API CALL'

@app.route('/api/image', methods = { 'POST' })
def api_image():
    if 'image' not in request.files:
        return 'No image was included in request', 400
    file = request.files['image']
    if file.filename == '':
        return 'File name was null', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #todo save filename to db
        return 'Successfully uploaded the image'
    return 'Issue saving image'






def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




if __name__ == '__main__':
    app.run()