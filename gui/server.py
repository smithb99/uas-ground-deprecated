import hashlib
import tkinter
import uuid

from .main import write_config, __config__


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


def login(ip, user, password):
    pass_hash = hash_password(password)

    if __config__["Server"].getboolean("RememberLogin"):
        write_config("Server", "ServerIp", ip)
        write_config("Server", "ServerUsername", user)
        write_config("Server", "ServerPassHash", pass_hash)
        write_config("Server", "ServerPassLen", len(password))

    pass # TODO Send to server for database check


def login_screen():
    root = tkinter.Tk()

    root.mainloop()
