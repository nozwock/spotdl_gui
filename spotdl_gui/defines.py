from pathlib import Path

import platformdirs

from . import version

CONFIG_DIR = Path(platformdirs.user_config_dir()).joinpath("spotdl_gui")
CONFIG_PATH = CONFIG_DIR.joinpath("config.pickle")

SPOTDL_FILE_FILTER = "SpotDL File (*.spotdl)"

SPOTDL_VERSION = version("spotdl")
