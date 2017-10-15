"""
image.py

This module provides the code associated with the image cropping GUI and some
backend connection code, such as getting and posting images.

Author:
    Braedon Smith <bhsmith1999@gmail.com>

Todo:
    126: Handle error when JSON is formatted incorrectly
    133: Cleanly exit by sending unprocessed images back to the server and
         destroying root
"""

import json
import tkinter
import tkinter.messagebox

from io import BytesIO
from PIL.ImageTk import PhotoImage

from gui.main import read_config

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

        self.root = tkinter.Toplevel(self.lower, name="imageHandler")
        self.canvas = tkinter.Canvas(self.root)

    def image_screen(self):
        """
        image_screen():  Handles GUI code for the image processing screen
        """

        self.root.title("Image Cropper")

        pop_button = tkinter.Button(self.root, text="New Image",
                                    command=self.pop)

        submit_button = tkinter.Button(self.root, text="Submit Image")
        exit_button = tkinter.Button(self.root, text="Disconnect",
                                     command=self.disconnect)

        self.root.geometry("{}x{}".format(
            read_config(self.config, "GUI", "WindowWidth"),
            read_config(self.config, "GUI", "WindowHeight"))
        )

        # root.grid_columnconfigure(1, minsize=) TODO minimum size - resolution

        pop_button.grid(row=0, column=0, padx=40, pady=10, sticky=tkinter.W)
        submit_button.grid(row=1, column=0, padx=40, pady=10, sticky=tkinter.W)
        exit_button.grid(row=2, column=0, padx=40, pady=10, sticky=tkinter.W)

        self.canvas.grid_bbox(column=1, row=0, col2=1, row2=4)

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

        return PhotoImage(BytesIO(requests.get(self.hostname + "/api/image/" +
                                               image_id, headers=headers)
                                  .content))

    def pop(self):
        """
        pop(): Draws the popped image
        """

        image = self.get_image()

        self.canvas.create_image((0, 0), image=image)

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

    def disconnect(self):
        """
        disconnect():  Cleanly exits the image crop window.
        """

        # TODO send images back to server

        self.root.destroy()
        self.lower.deiconify()
        self.lower.children["connectionConsole"].destroy()
