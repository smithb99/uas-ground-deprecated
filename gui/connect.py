"""
connect.py

This module provides the code associated with the server connection GUI and all
backend connection code, such as the login handler and uplink manager.

Author:
    Braedon Smith <bhsmith1999@gmail.com>
"""

import tkinter
import tkinter.messagebox

from gui.image import ImageHandler

import requests


class ConnectManager:
    """
    Class ConnectManager:

    Description:
        Handles code for displaying the connection status window and its
        associated functions.
    """

    def __init__(self, root, config, hostname):
        self.hostname = hostname
        self.lower = root
        self.config = config

        self.root = tkinter.Toplevel(self.lower, name="connectionConsole")

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

        try:
            response = requests.get(self.hostname + "/api", headers=headers)
            print(str(response.status_code))
        except requests.exceptions.MissingSchema:
            status.insert(0, "Error connecting to server. Failed to connect." +
                             " MissingSchema")
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

        if response.status_code == 200:
            message = self.hostname + " responded with HTTP 200 (OK). " +\
                      "Connection successful."

            self.lower.withdraw()
            self.image_screen()
        else:
            message = "Failed to connect to server."
            self.root.after(5000, self.root.destroy())

        # status.insert(tkinter.INSERT, message) TODO create console
        print(message)
        status.update_idletasks()

    def image_screen(self):
        """
        image_screen(): Handles code for launching the image editing screen.
        """

        image_manager = ImageHandler(self.lower, self.config, self.hostname)

        image_manager.image_screen()
