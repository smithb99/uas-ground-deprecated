import requests
import tkinter

from io import BytesIO
from PIL import Image
from requests.auth import HTTPDigestAuth


def connect_screen(self, hostname, username, password):
    root = tkinter.Toplevel(self)
    root.title("Connecting to Server...")

    status = tkinter.Text(root)

    response = requests.get(hostname, auth=HTTPDigestAuth(username, password))

    if response.status_code == 200:
        pass


def get_image():
    pass


def image_screen():
    pass


def post_image():
    pass
