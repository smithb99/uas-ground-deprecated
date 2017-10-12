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
    156: Stop hard-coding the window height and width and get the monitor size.

Author:
    Braedon Smith <bhsmith1999@gmail.com>
"""

import configparser
import os
import pathlib
import random

import tkinter
import tkinter.font
import tkinter.ttk

import gui.server

from PIL import Image, ImageTk

__version__ = "2.0.0"
__config__ = None

root = None
label = None
image = None

program_path = os.path.dirname(os.path.realpath(__file__))


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


def stop():
    """
    stop(): Stops the window and exits the program.
    """

    root.destroy()


def write_config(section, key, value):
    """
    write_config():  Writes a change in a configuration value

    section:  The section of the new value
    key:  The key of the new value
    value:  The value to assign to the key
    """

    __config__.set(section, key, value)
    __config__.set("GUI", "Version", __version__)


def main():
    """
    main():  Program entry point
    """

    # mode = __config__.getboolean("GUI", "Fullscreen")
    width = __config__.getint("GUI", "WindowWidth")
    height = __config__.getint("GUI", "WindowHeight")

    global root
    root = tkinter.Tk()

    root.title("Kansas State University UAS Client")
    root.geometry("{}x{}".format(str(width), str(height)))

    global image
    image = Image.open(
        os.path.join(program_path, "assets", "ksu" + str(random.randint(1, 2)) +
                     ".png")
    )

    # if mode:
    #     root.attributes("-fullscreen", True)
    #     image = resize_image(image, root.winfo_screenwidth())
    # else:
    #     root.attributes("-fullscreen", False)
    #     image = resize_image(image, width)

    photo = ImageTk.PhotoImage(image)

    global label
    label = tkinter.Label(root, width=width, height=height, image=photo,
                          anchor=tkinter.NW)

    # label.bind("<Configure>", on_configure)
    label.pack(fill=tkinter.BOTH, expand=tkinter.YES, side=tkinter.BOTTOM)

    tkinter.ttk.Style().configure("home.TButton", font=tkinter.font.Font(
        family="Helvetica", size=36, weight=tkinter.font.BOLD
    ))

    server_button = tkinter.ttk.Button(label, text="Connect to Server",
                                       style="home.TButton",
                                       command=lambda: gui.server.
                                       login_screen(root))

    exit_button = tkinter.ttk.Button(label, text="Exit", style="home.TButton",
                                     command=stop)

    exit_button.pack(anchor=tkinter.SW, side=tkinter.BOTTOM, padx=100, pady=50)

    server_button.pack(anchor=tkinter.SW, side=tkinter.BOTTOM, padx=100)

    root.mainloop()


if __name__ == "__main__":
    config_path = pathlib.Path(os.path.join(program_path, "auvsi-config.ini"))

    if not config_path.exists():
        config = configparser.ConfigParser()

        config["Server"] = {
            "ServerHostname": "",
            "ServerUsername": "",
            "ServerPassHash": "",
            "ServerPassLen": "",
            "RememberLogin": "false",
            "HashAlgorithm": "sha512"
        }

        config["GUI"] = {
            "Version": __version__,
            "WindowWidth": "960",  # TODO stop hard-coding
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
