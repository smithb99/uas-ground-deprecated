"""
connect.py

This module provides the code associated with the server connection GUI and all
backend connection code, such as the login handler and uplink manager.

Author:
    Braedon Smith <bhsmith1999@gmail.com>

Todo:
    56: Handle an error with a popup message
"""

import json
import tkinter

from io import BytesIO
from PIL import Image
from requests.auth import HTTPDigestAuth

import requests


class ConnectManager:
    """
    Class ConnectManager:

    Description:
        Handles code for displaying the connection status window and its
        associated functions.
    """

    def __init__(self, root, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.lower = root

    def connect_screen(self):
        """
        connect_screen(tkinter.Widget):

        Args:
            self: The parent widget of the window
        """

        root = tkinter.Toplevel(self.lower)
        root.title("Connecting to Server...")

        status = tkinter.Text(root)
        response = None

        headers = {
            'cache-control': "no-cache",
            'postman-token': "afe3920c-eb2e-f9e7-9293-660ca9bc801e"
        }

        try:
            response = requests.get(self.hostname, headers=headers,
                                    auth=HTTPDigestAuth(self.username,
                                                        self.password))
        except requests.exceptions.MissingSchema:
            pass  # TODO error popup

        if response.status_code == 200:
            status.insert(0, self.hostname + " responded with HTTP 200 (OK).")

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

    def image_screen(self):
        """
        image_screen(): Handles code for displaying the image editing screen.
        """

        pass

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

            if bool(int(image_json["has_odlc"])):
                new_json = '{"has_odlc":%d,"original_id":%d,"shape":%s,' +\
                           '"background_color":%s,"alphanumeric":%s,' +\
                           '"alphanumeric_color":%s,"orientation":%s}'
            else:
                new_json = '{"has_odlc": %d, "original_id": %d}' % (
                    image_json["has_odlc"], image_json["id"])

            requests.post(self.hostname, auth=(self.username, self.password),
                          json=new_json, data=image)
