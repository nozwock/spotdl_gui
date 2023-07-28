from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path

import platformdirs

from .defines import CONFIG_DIR, CONFIG_PATH


@dataclass
class Config:
    output_dir: Path

    @classmethod
    def load(cls) -> Config:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        if CONFIG_PATH.is_file():
            with open(CONFIG_PATH, "rb") as f:
                cfg = pickle.load(f)
                if not isinstance(cfg, Config):
                    raise Exception(f"Corrupted config: {CONFIG_PATH}")
                return cfg

        return Config(output_dir=Path())

    def store(self) -> None:
        with open(CONFIG_PATH, "wb") as f:
            pickle.dump(self, f)
