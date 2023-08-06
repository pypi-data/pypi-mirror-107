import subprocess
import os
import platform


def xopen(file_name=None):
    if file_name:
        pre_path = os.path.expanduser("~/Desktop/")
        new_path = pre_path + file_name
        if not os.path.exists(new_path):
            os.mkdir(new_path)
    else:
        new_path = os.getcwd()

    if platform.system() == "Windows":
        os.startfile(new_path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", new_path])
    else:
        subprocess.Popen(["xdg-open", new_path])

    return new_path + "/"