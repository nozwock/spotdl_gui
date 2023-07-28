from pathlib import Path

import platformdirs

CONFIG_DIR = Path(platformdirs.user_config_dir()).joinpath("spotdl_gui")
CONFIG_PATH = CONFIG_DIR.joinpath("config.pickle")
