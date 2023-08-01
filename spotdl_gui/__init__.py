from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except Exception:
    # Package isn't installed

    from pathlib import Path

    import tomllib

    with open(Path(__package__).parent.joinpath("pyproject.toml"), "rb") as f:
        _META = tomllib.load(f)

    __version__ = _META["tool"]["poetry"]["version"]
    del _META
