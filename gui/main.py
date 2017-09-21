import hashlib
import pathlib
import shutil
import tkinter

__version__ = "2.0.0"
__config_file__ = None


# TODO minor issue
def login(user, password):
    pass_hash = hashlib.sha512
    pass


def main():
    root = tkinter.Tk()

    root.mainloop()


if __name__ == "__main__":
    # TODO stop hardcoding and get execution directory
    program_path = pathlib.Path("./")
    config_path = pathlib.Path("./auvsi-" + __version__ + "-config.ini")

    if not config_path.exists():
        shutil.copyfile("./resources/auvsi-" + __version__ + "-config.ini",
                        "./auvsi-" + __version__ + "-config.ini")

    __config_file__ = (config_path, "r+")

    main()
