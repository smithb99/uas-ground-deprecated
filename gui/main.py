import configparser
import hashlib
import os
import pathlib
import tkinter
import uuid

__version__ = "2.0.0"
__config__ = None


def hash_password(password):
    # TODO minor issue
    algorithm = __config__["Server"]["HashAlgorithm"]
    algorithm = algorithm.lower()

    salt = uuid.uuid4().hex

    if algorithm == "md5":
        pass_hash = hashlib.md5(salt.encode() + password.encode())
    elif algorithm == "sha1":
        pass_hash = hashlib.sha1(salt.encode() + password.encode())
    elif algorithm == "sha224":
        pass_hash = hashlib.sha224(salt.encode() + password.encode())
    elif algorithm == "sha256":
        pass_hash = hashlib.sha256(salt.encode() + password.encode())
    elif algorithm == "sha384":
        pass_hash = hashlib.sha384(salt.encode() + password.encode())
    elif algorithm == "sha512":
        pass_hash = hashlib.sha512(salt.encode() + password.encode())
    else:
        pass_hash = hashlib.sha512(salt.encode() + password.encode())

    return pass_hash.hexdigest() + ":" + salt


def login(user, password):
    pass_hash = hash_password(password)

    pass

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
    config_path = pathlib.Path(program_path + "auvsi-config.ini")

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
            "WindowWidth": "",
            "WindowHeight": "",
            "Mode": "WINDOWED"
        }

        with open(config_path, "w") as config_file:
            config.write(config_file)
            config_file.close()
    else:
        __config__ = configparser.ConfigParser().read(config_path)

    main()
