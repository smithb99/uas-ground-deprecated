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
from json.decoder import JSONDecodeError
from PIL.ImageTk import PhotoImage

from gui.main import read_config

import requests


class ImageHandler:
    """
    Class ImageHandler

    Description:
        Handles code for getting, cropping, and posting images.
    """

    def __init__(self, root, config, hostname):
        self.lower = root
        self.config = config
        self.hostname = hostname

        self.root = tkinter.Toplevel(self.lower, name="imageHandler")
        self.canvas = tkinter.Canvas(self.root)

    def crop_image(self):
        pass

    def image_screen(self):
        """
        image_screen():  Handles GUI code for the image processing screen
        """

        self.root.title("Image Cropper")

        pop_button = tkinter.Button(self.root, text="New Image",
                                    command=lambda: self.draw_image())

        submit_button = tkinter.Button(self.root, text="Submit Image")
        exit_button = tkinter.Button(self.root, text="Disconnect",
                                     command=lambda: self.disconnect())

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

        response = requests.get(self.hostname + "/api/image")

        try:
            response_json = json.loads(response.json())
        except JSONDecodeError:
            return None

        if response.status_code not in (200, 204):
            tkinter.messagebox.showinfo("Error connecting to server",
                                        "Failed to connect. Host responded "
                                        + "with code " +
                                        str(response.status_code))

            return None

        try:
            image_id = response_json["id"]
        except KeyError:
            return None

        headers = {
            'cache-control': "no-cache",
            'postman-token': "afe3920c-eb2e-f9e7-9293-660ca9bc801e"
        }

        return PhotoImage(BytesIO(requests.get(self.hostname + "/api/image/"
                                               + image_id, headers=headers)
                                  .content))

    def draw_image(self):
        """
        draw_image(): Draws the popped image
        """

        image = self.get_image()

        if image is not None:
            self.canvas.create_image((0, 0), image=image)
        else:
            tkinter.messagebox.showerror("No image found", "Server did not " +
                                         "return an image. Please wait for a " +
                                         "new one to be taken.")

    def post_image(self, images):
        """
        post_image(str, str, str, PIL.Image{}): Posts a series of cropped images
                                                to the server.

        Args:
            images: A dictionary of images and JSON data to post to the server

        Returns: The HTTP response code
        """

        for image in images:
            image_json = json.loads(images[image])

            requests.post(self.hostname, json=image_json, data=image)

            # TODO handle errors when JSON is formatted incorrectly

    def disconnect(self):
        """
        disconnect():  Cleanly exits the image crop window.
        """

        # TODO log any unprocessed images

        self.root.destroy()
        self.lower.deiconify()
        self.lower.children["connectionConsole"].destroy()
