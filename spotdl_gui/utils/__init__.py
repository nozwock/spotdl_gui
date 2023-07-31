import os
import platform
import subprocess
from pathlib import Path
from typing import Any


def open_default(path: Path) -> None:
    system = platform.system()
    if system == "Windows":
        os.startfile(path)  # type: ignore
    elif system == "Linux":
        subprocess.Popen(["xdg-open", str(path.absolute())])
    elif system == "Darwin":
        subprocess.Popen(["open", str(path.absolute())])
    else:
        ...


def override_map_values(
    key_from: dict[str, Any], values_from: dict[str, Any]
) -> dict[str, Any]:
    """
    Returns a map identical in structure to `keys_from` but using the values from `values_from`.
    """

    out = {}
    override_keys = values_from.keys()
    for k in key_from.keys():
        if k in override_keys:
            out[k] = values_from[k]

    return out
