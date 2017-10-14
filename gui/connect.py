"""
connect.py

This module provides the code associated with the server connection GUI and all
backend connection code, such as the login handler and uplink manager.

Author:
    Braedon Smith <bhsmith1999@gmail.com>

Todo:
    56: Handle an error with a popup message
"""

import requests
import tkinter

from io import BytesIO
from PIL import Image
from requests.auth import HTTPDigestAuth


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

        try:
            response = requests.get(self.hostname,
                                    auth=HTTPDigestAuth(self.username,
                                                        self.password))

        except requests.exceptions.MissingSchema:
            pass  # TODO error popup

        if response.status_code == 200:
            pass

    def get_image(self):
        """
        get_image(): Pops an image from the queue on the server.

        Returns: the image from the server
        """

        pass

    def image_screen(self):
        """
        image_screen(): Handles code for displaying the image editing screen.
        """

        pass

    def post_image(self, hostname, username, password, image):
        """
        post_image(str, str, str, PIL.Image[]): Posts an array of cropped images
                                                to the server.

        Args:
            hostname: The fully qualified URI of the server
            username: The username of the user on the server
            password: The password for the user

        Returns: The HTTP response code
        """

        pass
