"""
server.py

This module provides the code associated with the server connection GUI.

Author:
    Braedon Smith <bhsmith1999@gmail.com>
"""

import tkinter

from gui.connect import ConnectManager
from gui.main import write_config


class ServerManager:
    """
    Class ServerManager:

    Description:
        Handles the code for displaying the server GUI screen and associated
        functions.
    """

    def __init__(self, root, config, config_path):
        self.config = config
        self.lower = root
        self.config_path = config_path

        self.root = tkinter.Toplevel(self.lower)

    def connect_screen(self, config_path, hostname, user, password, is_checked):
        """
        connect_screen(str, str, str, tkinter.BooleanVar):  Creates the
                                                            connection status
                                                            screen object

        Args:
            config_path: The path to the configuration file
            hostname: The fully qualified hostname of the target server.
            user: The user on the target server.
            password:  The password for the above user.
            is_checked:  Whether the remember me checkbutton is checked
        """

        if is_checked.get():
            write_config(self.config, config_path, "Server", "RememberLogin",
                         "true")

        if self.config["Server"].getboolean("RememberLogin"):
            write_config(self.config, config_path, "Server", "ServerHostname",
                         hostname)
            write_config(self.config, config_path, "Server", "ServerUsername",
                         user)
            write_config(self.config, config_path, "Server", "ServerPassword",
                         password)

        connect_manager = ConnectManager(self.lower, self.config, hostname,
                                         user, password)

        connect_manager.connect_screen()
        self.root.destroy()

    def login_screen(self):
        """
        login_screen(): Provides the GUI for handling login credentials.
        """

        self.root.title("Log In")

        hostname_label = tkinter.Label(self.root, text="Hostname: ")
        hostname_entry = tkinter.Entry(self.root)

        username_label = tkinter.Label(self.root, text="Username: ")
        username_entry = tkinter.Entry(self.root)

        password_label = tkinter.Label(self.root, text="Password: ")
        password_entry = tkinter.Entry(self.root, show="*")

        if self.config.getboolean("Server", "RememberLogin"):
            hostname_entry.insert(0,
                                  self.config["Server"]["ServerHostname"])

            username_entry.insert(0,
                                  self.config["Server"]["ServerUsername"])

            password_entry.insert(0,
                                  self.config["Server"]["ServerPassword"])

        is_checked = tkinter.BooleanVar()
        remember_me = tkinter.Checkbutton(self.root, variable=is_checked,
                                          text="Remember me on this computer")

        if self.config["Server"].getboolean("RememberLogin"):
            remember_me.select()

        submit_button = tkinter.Button(self.root, text="Log In", command=lambda:
                                       self.connect_screen(
                                           self.config_path,
                                           hostname_entry.get(),
                                           username_entry.get(),
                                           password_entry.get(), is_checked)
                                       )

        hostname_label.grid(row=0, column=0, pady=5)
        hostname_entry.grid(row=0, column=1, pady=5)

        username_label.grid(row=1, column=0, pady=5)
        username_entry.grid(row=1, column=1, pady=5)

        password_label.grid(row=2, column=0, pady=5)
        password_entry.grid(row=2, column=1, pady=5)

        submit_button.grid(row=3, column=0, pady=10)
        remember_me.grid(row=3, column=1, pady=10)
