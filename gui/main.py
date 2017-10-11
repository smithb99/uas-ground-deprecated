import configparser
import os
import pathlib
import random
import tkinter

from PIL import Image, ImageTk

__version__ = "2.0.0"
__config__ = None

root = None


def stop():
    root.destroy()


def read_config(section, key):
    return __config__.get(section, key)


def resize_image(image, width):
    width_percent = (width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(width_percent)))

    return image.resize((width, h_size), Image.ANTIALIAS)


def write_config(section, key, value):
    __config__.set(section, key, value)


def main():
    mode = __config__.getboolean("GUI", "Fullscreen")
    width = read_config("GUI", "WindowWidth")
    height = read_config("GUI", "WindowHeight")

    global root
    root = tkinter.Tk()

    root.title("Kansas State University UAS Client")

    image = Image.open("assets/ksu" + str(random.randint(1, 2)) + ".png")

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

    server_button.grid(row=0)
    exit_button.grid(row=1)

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
            "Fullscreen": "true"
        }

        with open(config_path, "w") as config_file:
            config.write(config_file)
            config_file.close()
    else:
        __config__ = configparser.ConfigParser(allow_no_value=True)
        __config__.read(config_path)

    main()
