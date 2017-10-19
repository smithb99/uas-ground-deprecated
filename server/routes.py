from flask import request

from Database.initialize import app
from Controllers import ImageController, JudgeController

app.config['judge_token'] = JudgeController.authenticate()

# GET /api
@app.route('/api')
def api_get_status():
    return "Status: OK", 200

#GET /api/judge/token
@app.route('/api/judge/token')
def api_get_judge_token():
    token = JudgeController.authenticate()
    if token is not None:
        app.config['judge_token'] = token
        return "", 204
    else:
        return "Issue retrieving new token", 400

# GET /api/image
@app.route('/api/image')
def api_get_image():
    return ImageController.get_raw_image()

# GET /api/image/<int:id>
@app.route('/api/image/<int:id>')
def api_get_image_by_id(id):
    return ImageController.get_image_by_id(id)

# POST /api/image
@app.route('/api/image', methods = { 'POST' })
def api_post_raw_image():
    return ImageController.post_raw_image(request)

# POST /api/image/cropped
@app.route('/api/image/cropped', methods = { 'POST' })
def api_post_processed_image():
    token = app.config['judge_token']
    return ImageController.post_processed_image(request, token)

