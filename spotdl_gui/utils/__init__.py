import os
import platform
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

is_frozen = hasattr(sys, "frozen") and hasattr(sys, "_MEIPASS")


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

    out = deepcopy(key_from)
    override_keys = values_from.keys()
    for k in key_from.keys():
        if k in override_keys:
            out[k] = values_from[k]

    return out


def shorten_string(
    txt: str, width: int = 40, suffix: str = "...", lshorten: bool = False
) -> str:
    if lshorten:
        return (
            suffix + txt[len(txt) - width :] if len(txt) > width + len(suffix) else txt
        )
    else:
        return txt[: width + 1] + suffix if len(txt) > width + len(suffix) else txt


def with_extension(path: Path, ext: str) -> Path:
    if not path.suffix or path.suffix.lower() == ext:
        path = path.with_suffix(ext)
    else:
        path = path.with_name(path.name + ext)

    return path
