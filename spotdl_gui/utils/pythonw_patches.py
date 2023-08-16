import platform
import subprocess
import sys

from . import is_frozen

# Patches for pythonw

__all__: list[str] = []


class PythonwPopen(subprocess.Popen):
    def __init__(self, *args, **kwargs):
        if subprocess._mswindows:
            if len(args) >= 14:
                args[13] = subprocess.CREATE_NO_WINDOW | args[13]
            else:
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW | kwargs.get(
                    "creationflags", 0
                )

        super().__init__(*args, **kwargs)


if platform.system() == "Windows" and (
    is_frozen or (not is_frozen and sys.executable.find("pythonw.exe") != -1)
):  # Couldn't find a way to know if a frozen app is windowed
    # So this will apply to both --console and --windowed
    subprocess.Popen = PythonwPopen  # type: ignore[misc]
