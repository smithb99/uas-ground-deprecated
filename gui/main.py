#!/usr/bin/env python3

"""
main.py

This module provides the program entry point, main function, and home screen GUI
objects.  This module should be run as follows.

Example:
    $ python main.py

Todo:
    153: Stop hard-coding the window height and width and get the monitor size.

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

import gui.connect
import gui.metadata
import gui.server

from PIL import Image, ImageTk


class Main:
    """
    Class Main:

    Description:
        The main class responsible for handling the GUI main screen and calling
        associated functions.
    """
    def __init__(self, config_handle, path):
        self.config = config_handle
        self.program_path = path

        self.root = tkinter.Tk()
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        write_config(config_handle, CONFIG_PATH, "GUI", "WindowWidth", width)
        write_config(config_handle, CONFIG_PATH, "GUI", "WindowHeight", height)

        self.main()

    def login_screen(self):
        """
        login_screen():  Creates the server login screen object
        """

        server_manager = gui.server.ServerManager(self.root, self.config,
                                                  CONFIG_PATH)
        server_manager.login_screen()

    def stop(self):
        """
        stop(): Stops the window and exits the program.
        """

        self.root.destroy()

    def main(self):
        """
        main():  Program entry point
        """

        # mode = __config__.getboolean("GUI", "Fullscreen")
        width = self.config.getint("GUI", "WindowWidth")
        height = self.config.getint("GUI", "WindowHeight")

        self.root.title("Kansas State University UAS Client")
        self.root.geometry("{}x{}".format(str(width), str(height)))

        image = Image.open(
            os.path.join(self.program_path, "assets", "ksu" +
                         str(random.randint(1, 2)) + ".png")
        )

        # if mode:
        #     root.attributes("-fullscreen", True)
        #     image = resize_image(image, root.winfo_screenwidth())
        # else:
        #     root.attributes("-fullscreen", False)
        #     image = resize_image(image, width)

        photo = ImageTk.PhotoImage(image)

        label = tkinter.Label(self.root, width=width, height=height,
                              image=photo, anchor=tkinter.NW)

        # label.bind("<Configure>", on_configure)
        label.pack(fill=tkinter.BOTH, expand=tkinter.YES, side=tkinter.BOTTOM)

        tkinter.ttk.Style().configure("home.TButton", font=tkinter.font.Font(
            family="Helvetica", size=36, weight=tkinter.font.BOLD
        ))

        server_button = tkinter.ttk.Button(label, text="Connect to Server",
                                           style="home.TButton",
                                           command=lambda: self.login_screen())

        exit_button = tkinter.ttk.Button(label, text="Exit",
                                         style="home.TButton", command=self.stop
                                         )

        exit_button.pack(anchor=tkinter.SW, side=tkinter.BOTTOM, padx=100,
                         pady=50)

        server_button.pack(anchor=tkinter.SW, side=tkinter.BOTTOM, padx=100)

        self.root.mainloop()


def read_config(config_handle, section, key):
    """
    read_config(configparser.ConfigParser, str, str): Reads data from an INI
                                                      configuration file.

    Args:
        config_handle:  The ConfigParser responsible for the specific INI file
                        being read
        section:  The INI section to search for
        key:  The INI key to search within the section for

    Returns:
        The value of the specified key
    """

    return config_handle.get(section, key)


def write_config(config_handle, config_path, section, key, value):
    """
    write_config(configparser.ConfigParser, str, str, str):  Writes a change to
                                                             a configuration
                                                             value

    Args:
        config_handle:  The ConfigParser responsible for the specific INI file
                        being written to
        config_path:  The path to the file being written to
        section:  The section of the new value
        key:  The key of the new value
        value:  The value to assign to the key
    """

    config_handle.set(section, key, value)
    config_handle.set("GUI", "Version", gui.metadata.__version__)

    with open(config_path, "w") as conf:
        config_handle.write(conf)


if __name__ == "__main__":
    PROGRAM_PATH = os.path.dirname(os.path.realpath(__file__))
    CONFIG_PATH = pathlib.Path(os.path.join(PROGRAM_PATH,
                                            "auvsi-config.ini"))

    if not CONFIG_PATH.exists():
        CONFIG = configparser.ConfigParser()

        CONFIG["Server"] = {
            "ServerHostname": "",
            "ServerUsername": "",
            "ServerPassword": "",
            "RememberLogin": "false",
        }

        CONFIG["GUI"] = {
            "Version": gui.metadata.__version__,
            "WindowWidth": "",
            "WindowHeight": "",
            "Fullscreen": "true"
        }

        with open(CONFIG_PATH, "w") as config_file:
            CONFIG.write(config_file)
            config_file.close()
    else:
        CONFIG = configparser.ConfigParser(allow_no_value=True)
        CONFIG.read(CONFIG_PATH)

    MAIN = Main(CONFIG, PROGRAM_PATH)
