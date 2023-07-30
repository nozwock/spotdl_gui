from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from pathlib import Path

from .defines import CONFIG_DIR, CONFIG_PATH


@dataclass
class Config:
    output_dir: Path = field(default_factory=Path)

    @classmethod
    def load(cls) -> Config:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        if CONFIG_PATH.is_file():
            with open(CONFIG_PATH, "rb") as f:
                cfg = pickle.load(f)
                if not isinstance(cfg, cls):
                    raise Exception(f"Corrupted config: {CONFIG_PATH}")
                return cfg

        return cls()

    def store(self) -> None:
        with open(CONFIG_PATH, "wb") as f:
            pickle.dump(self, f)
