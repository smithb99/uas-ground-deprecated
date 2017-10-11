#!/usr/bin/env python3

"""
main.py

This module provides the program entry point, main function, and home screen GUI
objects.  This module should be run as follows.

Example:
    $ python main.py

Attributes:
    __version__ (str): Stores the version number of the program.
    __config__ (ConfigParser): Stores a reference to the configuration handler
    root (Tk): The root Tk object in command of the GUI
    program_path: A reference to the current execution directory

Todo:
    147: Stop hardcoding the window height and width and get the monitor size.

Author:
    Braedon Smith <bhsmith1999@gmail.com>
"""

import configparser
import os
import pathlib
import random
import tkinter

from PIL import Image, ImageTk

__version__ = "2.0.0"
__config__ = None

root = None
program_path = os.path.dirname(os.path.realpath(__file__))


def stop():
    """
    stop(): Stops the window and exits the program.
    """
    root.destroy()


def read_config(section, key):
    """
    read_config(): Reads data from a configuration file.

    Args:
        section:  The INI section to search for
        key:  The INI key to search within the section for

    Returns:
        The value of the specified key
    """
    return __config__.get(section, key)


def resize_image(image, width):
    """
    resize_image():  Resizes an image using PIL.  Will maintain the original
    picture's aspect ratio.

    image:  the image to be resized
    width:  the new width of the image

    Returns:
         The resized image
    """
    width_percent = (width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(width_percent)))

    return image.resize((width, h_size), Image.ANTIALIAS)


def write_config(section, key, value):
    """
    write_config():  Writes a change in a configuration value

    section:  The section of the new value
    key:  The key of the new value
    value:  The value to assign to the key
    """
    __config__.set(section, key, value)


def main():
    """
    main():  Program entry point
    """
    mode = __config__.getboolean("GUI", "Fullscreen")
    width = read_config("GUI", "WindowWidth")
    height = read_config("GUI", "WindowHeight")

    global root
    root = tkinter.Tk()

    root.title("Kansas State University UAS Client")

    image = Image.open(
        os.path.join(program_path, "assets", "ksu" + str(random.randint(1, 2)) +
                     ".png")
    )

    if mode:
        root.attributes("-fullscreen", True)
        image = resize_image(image, root.winfo_screenwidth())
    else:
        root.attributes("-fullscreen", False)
        image = resize_image(image, width)

    photo = ImageTk.PhotoImage(image)

    label = tkinter.Label(root, width=width, height=height, image=photo,
                          anchor=tkinter.NW)

    label.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    server_button = tkinter.Button(label, text="Connect to Server")
    exit_button = tkinter.Button(label, text="Exit", command=stop)

    server_button.grid(row=0, sticky=tkinter.SW)
    exit_button.grid(row=1, sticky=tkinter.SW)

    root.mainloop()


if __name__ == "__main__":
    config_path = pathlib.Path(os.path.join(program_path, "auvsi-config.ini"))

    if not config_path.exists():
        config = configparser.ConfigParser()

        config["Server"] = {
            "ServerIp": "",
            "ServerUsername": "",
            "ServerPassHash": "",
            "ServerPassLen": "",
            "RememberLogin": "false",
            "HashAlgorithm": "sha512"
        }

        config["GUI"] = {
            "Version": __version__,
            "WindowWidth": "960",  # TODO stop hardcoding
            "WindowHeight": "540",
            "Fullscreen": "true"
        }

        with open(config_path, "w") as config_file:
            config.write(config_file)
            config_file.close()
    else:
        __config__ = configparser.ConfigParser(allow_no_value=True)
        __config__.read(config_path)

    main()
