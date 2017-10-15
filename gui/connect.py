"""
connect.py

This module provides the code associated with the server connection GUI and all
backend connection code, such as the login handler and uplink manager.

Author:
    Braedon Smith <bhsmith1999@gmail.com>

Todo:
    61: Handle an error when HTTP returns something other than 200
"""

import tkinter
import tkinter.messagebox

from requests.auth import HTTPDigestAuth
from .image import ImageHandler

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
        root.title("Server Manager Console")

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
            tkinter.messagebox.showinfo("Error connecting to server",
                                        "Failed to connect. Host responded " +
                                        "with code " + response.status_code)

        if response.status_code == 200:
            status.insert(0, self.hostname + " responded with HTTP 200 (OK).")
            self.lower.withdraw()
            self.image_screen()

    def image_screen(self):
        """
        image_screen(): Handles code for launching the image editing screen.
        """

        image_manager = ImageHandler(self.lower, self.hostname, self.username,
                                     self.password)

        image_manager.image_screen()
