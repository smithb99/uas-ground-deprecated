from flask import request

from Database.initialize import app
from Controllers import ImageController


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
    return ImageController.post_processed_image(request)
