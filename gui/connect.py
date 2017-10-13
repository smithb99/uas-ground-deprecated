"""
connect.py

This module provides the code associated with the server connection GUI and all
backend connection code, such as the login handler and uplink manager.

Author:
    Braedon Smith <bhsmith1999@gmail.com>
"""

import requests
import tkinter

from io import BytesIO
from PIL import Image
from requests.auth import HTTPDigestAuth


def connect_screen(self, hostname, username, password):
    """
    connect_screen(tkinter.Widget, str, str, str):

    Args:
        self: The parent widget of the window
        hostname: The fully qualified URI of the server
        username: The username of the user on the server
        password: The password for the user
    """

    root = tkinter.Toplevel(self)
    root.title("Connecting to Server...")

    status = tkinter.Text(root)
    response = None

    try:
        response = requests.get(hostname, auth=HTTPDigestAuth(username, password))
    except requests.exceptions.MissingSchema:
        pass  # TODO error popup

    if response.status_code == 200:
        pass


def get_image():
    """
    get_image(): Pops an image from the queue on the server.

    Returns: the image from the server
    """

    pass


def image_screen():
    """
    image_screen(): Handles code for displaying the image editing screen.
    """

    pass


def post_image(hostname, username, password, image):
    """
    post_image(str, str, str, PIL.Image[]): Posts an array of cropped images to
                                            the server.

    Args:
        hostname: The fully qualified URI of the server
        username: The username of the user on the server
        password: The password for the user

    Returns: The HTTP response code
    """

    pass
