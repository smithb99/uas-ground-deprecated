"""
server.py

This module provides the code associated with the server connection GUI.

Author:
    Braedon Smith <bhsmith1999@gmail.com>
"""

import tkinter

from .connect import ConnectManager
from .main import write_config


class ServerManager:
    """
    Class ServerManager:

    Description:
        Handles the code for displaying the server GUI screen and associated
        functions.
    """

    def __init__(self, root, config):
        self.__config__ = config
        self.lower = root

    def connect_screen(self, hostname, user, password):
        """
        connect_screen(str, str, str):  Creates the connection status screen
                                        object

        Args:
            hostname: The fully qualified hostname of the target server.
            user: The user on the target server.
            password:  The password for the above user.
        """

        if self.__config__["Server"].getboolean("RememberLogin"):
            write_config(self.__config__, "Server", "ServerHostname", hostname)
            write_config(self.__config__, "Server", "ServerUsername", user)
            write_config(self.__config__, "Server", "ServerPassword", password)
            write_config(self.__config__, "Server", "ServerPassLen",
                         len(password))

        connect_manager = ConnectManager(self.lower, hostname, user, password)
        connect_manager.connect_screen()

    def login_screen(self):
        """
        login_screen(): Provides the GUI for handling login credentials.
        """

        root = tkinter.Toplevel(self.lower)
        root.title("Log In")

        hostname_label = tkinter.Label(root, text="Hostname: ")
        hostname_entry = tkinter.Entry(root)

        username_label = tkinter.Label(root, text="Username: ")
        username_entry = tkinter.Entry(root)

        password_label = tkinter.Label(root, text="Password: ")
        password_entry = tkinter.Entry(root, show="*")

        submit_button = tkinter.Button(root, text="Log In", command=lambda:
                                       self.connect_screen(
                                           hostname_entry.get(),
                                           username_entry.get(),
                                           password_entry.get())
                                       )

        remember_me = tkinter.Checkbutton(root,
                                          text="Remember me on this computer")

        hostname_label.grid(row=0, column=0, pady=5)
        hostname_entry.grid(row=0, column=1, pady=5)

        username_label.grid(row=1, column=0, pady=5)
        username_entry.grid(row=1, column=1, pady=5)

        password_label.grid(row=2, column=0, pady=5)
        password_entry.grid(row=2, column=1, pady=5)

        submit_button.grid(row=3, column=0, pady=10)
        remember_me.grid(row=3, column=1, pady=10)
