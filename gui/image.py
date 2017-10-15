"""
image.py

This module provides the code associated with the image cropping GUI and some
backend connection code, such as getting and posting images.

Author:
    Braedon Smith <bhsmith1999@gmail.com>

Todo:
    109: Handle error when JSON is formatted incorrectly
    116: Cleanly exit by sending unprocessed images back to the server and
         destroying root
"""

import json
import tkinter
import tkinter.messagebox

from io import BytesIO
from PIL import Image

from .main import read_config

import requests


class ImageHandler:
    """
    Class ImageHandler

    Description:
        Handles code for getting, cropping, and posting images.
    """

    def __init__(self, root, config, hostname, username, password):
        self.lower = root
        self.config = config
        self.hostname = hostname
        self.username = username
        self.password = password

    def image_screen(self):
        """
        image_screen():  Handles GUI code for the image processing screen
        """
        root = tkinter.Toplevel(self.lower)
        root.title("Crop Image")

        pop_button = tkinter.Button(root, text="New Image")
        submit_button = tkinter.Button(root, text="Submit Image")
        exit_button = tkinter.Button(root, text="Exit", command=self.stop())

        image_canvas = tkinter.Canvas(root)

        root.geometry("{}x{}".format(
            read_config(self.config, "GUI", "WindowWidth"),
            read_config(self.config, "GUI", "WindowHeight"))
        )

        pop_button.grid(row=0, column=0)
        submit_button.grid(row=1, column=0)
        exit_button.grid(row=2, column=0)

        image_canvas.grid(row=0, column=1)

    def get_image(self):
        """
        get_image(): Pops an image from the queue on the server.

        Returns: the image from the server
        """

        response = requests.get(self.hostname + "/api/image",
                                auth=(self.username, self.password))

        response_json = json.loads(response.json())

        if response.status_code != 200:
            tkinter.messagebox.showinfo("Error connecting to server",
                                        "Failed to connect. Host responded " +
                                        "with code " + response.status_code)

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

            # TODO handle errors when JSON is formatted incorrectly

    def stop(self):
        """
        stop():  Cleanly exits the application.
        """

        pass  # TODO clean exit - send images back to server and destroy root
