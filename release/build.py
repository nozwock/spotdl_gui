import platform
from pathlib import Path

import PyInstaller.__main__

from spotdl_gui import __version__

root_path = Path(__file__).parent.parent
on_macos = platform.system() == "Darwin"
icon = "icon.icns" if on_macos else "icon.ico"


args = [
    "--name",
    f"spotdl_gui-{__version__}-{platform.machine()}-{platform.system()}",
    "--noupx",
    "--onedir",
    "--windowed",
    "--noconfirm",
    "--collect-data",
    "pykakasi",
    "--collect-data",
    "ytmusicapi",
    "--copy-metadata",
    "spotdl_gui",
    "--copy-metadata",
    "spotdl",
    "-i",
    str(root_path / f"release/resources/{icon}"),
    "spotdl_gui/__main__.py",
]

if not on_macos:
    args.extend(
        [
            "--splash",
            str(root_path / "release/resources/splash.png"),
        ]
    )

PyInstaller.__main__.run(args)
