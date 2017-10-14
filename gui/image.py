"""
image.py

This module provides the code associated with the image cropping GUI and some
backend connection code, such as getting and posting images.

Author:
    Braedon Smith <bhsmith1999@gmail.com>

Todo:
    50: Handle error when JSON is formatted incorrectly
"""

import json

from io import BytesIO
from PIL import Image

import requests


class ImageHandler:
    """
    Class ImageHandler

    Description:
        Handles code for getting, cropping, and posting images.
    """

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def image_screen(self):
        """
        image_screen():  Handles GUI code for the image processing screen
        """
        pass

    def get_image(self):
        """
        get_image(): Pops an image from the queue on the server.

        Returns: the image from the server
        """

        response_json = json.loads(requests.get(self.hostname + "/api/image")
                                   .json())
        # TODO handle exception

        image_id = response_json["id"]

        headers = {
            'cache-control': "no-cache",
            'postman-token': "afe3920c-eb2e-f9e7-9293-660ca9bc801e"
        }

        return Image.open(BytesIO(requests.get(self.hostname + "/api/image/" +
                                               image_id, headers=headers)
                                  .content))

    def post_image(self, images):
        """
        post_image(str, str, str, PIL.Image{}): Posts an array of cropped images
                                                to the server.

        Args:
            images: A dictionary of images and JSON data to post to the server

        Returns: The HTTP response code
        """

        for image in images:
            image_json = json.loads(images[image])

            requests.post(self.hostname, auth=(self.username, self.password),
                          json=image_json, data=image)
