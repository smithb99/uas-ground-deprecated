"""
connect.py

This module provides the code associated with the server connection GUI and all
backend connection code, such as the login handler and uplink manager.

Author:
    Braedon Smith <bhsmith1999@gmail.com>

Todo:
    79:  Wait for Kyle to add the test endpoint so actual error checking can
         happen
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

    def __init__(self, root, config, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.lower = root
        self.config = config

        self.root = tkinter.Toplevel(self.lower)

    def connect_screen(self):
        """
        connect_screen(tkinter.Widget):

        Args:
            self: The parent widget of the window
        """

        self.root.title("Server Manager Console")

        status = tkinter.Text(self.root)
        response = None

        headers = {
            'cache-control': "no-cache",
            'postman-token': "afe3920c-eb2e-f9e7-9293-660ca9bc801e"
        }

        # try:
        #     response = requests.get(self.hostname, headers=headers,
        #                             auth=HTTPDigestAuth(self.username,
        #                                                 self.password))
        # except requests.exceptions.MissingSchema:
    #     status.insert(0, "Error connecting to server. Failed to connect." +
        #                  " MissingSchema")

        # if response.status_code == 200:
        #     message = self.hostname + " responded with HTTP 200 (OK). " +\
        #               "Connection successful."

        #     self.lower.withdraw()
        #     self.image_screen()
        # elif response.status_code != 200:
        #     message = self.hostname + " responded with HTTP " +\
        #               str(response.status_code) + "."
        # else:
        #     message = "Failed to connect to server."

        # status.insert(0, message) TODO wait for Kyle to add the test endpoint

        try:
            response = requests.get(self.hostname, headers=headers,
                                    auth=HTTPDigestAuth(self.username,
                                                        self.password))
        except requests.exceptions.ConnectTimeout:
            status.insert(tkinter.INSERT, "Error connecting to server. " +
                                          "Connection timed out." +
                                          " requests.exceptions.ConnectTimeout")
        except requests.exceptions.InvalidHeader:
            status.insert(tkinter.INSERT, "Error connecting to server. " +
                                          "Invalid header." +
                                          " requests.exceptions.InvalidHeader")
        except requests.exceptions.InvalidSchema:
            status.insert(tkinter.INSERT, "Error connecting to server. " +
                                          "Invalid schema." +
                                          " requests.exceptions.InvalidSchema")
        except requests.exceptions.InvalidURL:
            status.insert(tkinter.INSERT, "Error connecting to server. " +
                                          "Invalid URL." +
                                          " requests.exceptions.InvalidURL")

        if response.status_code is not None:
            status.insert(tkinter.INSERT, self.hostname + " responded with " +
                          "HTTP " + str(response.status_code) + ".")

            self.lower.withdraw()
            self.image_screen()
        else:
            status.insert(0, self.hostname + " did not respond.")
            self.root.after(5000, self.root.destroy())

    def image_screen(self):
        """
        image_screen(): Handles code for launching the image editing screen.
        """

        image_manager = ImageHandler(self.lower, self.config, self.hostname,
                                     self.username, self.password)

        image_manager.image_screen()
