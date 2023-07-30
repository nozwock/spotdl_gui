import os
import platform
import subprocess
from pathlib import Path


def open_default(path: Path) -> None:
    system = platform.system()
    if system == "Windows":
        os.startfile(path)
    elif system == "Linux":
        subprocess.Popen(["xdg-open", str(path.absolute())])
    elif system == "Darwin":
        subprocess.Popen(["open", str(path.absolute())])
    else:
        ...
