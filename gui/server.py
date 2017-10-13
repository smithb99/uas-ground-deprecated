"""
server.py

This module provides the code associated with the server connection GUI and some
backend connection code, such as a login handler and uplink manager.

Todo:
    40: Minor issue - Handle logins
    84: Send to server for database check

Author:
    Braedon Smith <bhsmith1999@gmail.com>
"""

import tkinter

from .main import read_config, write_config, __config__


def login(hostname, user, password):
    """
    login(str, str, str):  Logs the user into the server

    Args:
        hostname: The textual representation of the server IP address
        user: The username to be accessed
        password: The password for the username

    Returns:
         TODO
    """

    if __config__["Server"].getboolean("RememberLogin"):
        write_config("Server", "ServerHostname", hostname)
        write_config("Server", "ServerUsername", user)
        write_config("Server", "ServerPassword", password)
        write_config("Server", "ServerPassLen", len(password))

    pass  # TODO Send to server for database check


def login_screen(self):
    """
    login_screen(): Provides the GUI for handling login credentials.
    """

    root = tkinter.Toplevel(self)
    root.title("Log In")

    hostname_label = tkinter.Label(root, text="Hostname: ")
    hostname_entry = tkinter.Entry(root)

    username_label = tkinter.Label(root, text="Username: ")
    username_entry = tkinter.Entry(root)

    password_label = tkinter.Label(root, text="Password: ")
    password_entry = tkinter.Entry(root, show="*")

    submit_button = tkinter.Button(root, text="Log In")
    remember_me = tkinter.Checkbutton(root, text="Remember me on this computer")

    hostname_label.grid(row=0, column=0, pady=5)
    hostname_entry.grid(row=0, column=1, pady=5)

    username_label.grid(row=1, column=0, pady=5)
    username_entry.grid(row=1, column=1, pady=5)

    password_label.grid(row=2, column=0, pady=5)
    password_entry.grid(row=2, column=1, pady=5)

    submit_button.grid(row=3, column=0, pady=10)
    remember_me.grid(row=3, column=1, pady=10)
