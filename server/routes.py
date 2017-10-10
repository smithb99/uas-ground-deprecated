import os
from flask import jsonify, request, send_from_directory
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException, NotFound
import uuid

from Database.initialize import app
from Models.Cropped import Cropped
from Models.Image import Image
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
