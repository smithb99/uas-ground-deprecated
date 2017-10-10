import configparser
import os
import pathlib
import tkinter

__version__ = "2.0.0"
__config__ = None


def write_config(section, key, value):
    __config__.set(section, key, value)


def main():
    root = tkinter.Tk()
    root.title("Kansas State University UAS Client")

    button_frame = tkinter.Frame(root)

    server_button = tkinter.Button(root, text="Connect to Server")
    exit_button = tkinter.Button(root, text="Exit")

    button_frame.pack()
    server_button.pack()
    exit_button.pack()

    root.mainloop()


if __name__ == "__main__":
    program_path = os.path.dirname(os.path.realpath(__file__))
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
            "WindowWidth": "",
            "WindowHeight": "",
            "Mode": "WINDOWED"
        }

        with open(config_path, "w") as config_file:
            config.write(config_file)
            config_file.close()
    else:
        __config__ = configparser.ConfigParser(allow_no_value=True).read(
            config_path
        )

    main()
