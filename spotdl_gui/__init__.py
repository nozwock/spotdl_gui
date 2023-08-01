from importlib.metadata import version

try:
    __version__ = version(__package__)
except Exception:
    # Package isn't installed

    def pkg_version() -> str | None:
        from pathlib import Path

        import tomllib

        with open(Path(__package__).parent.joinpath("pyproject.toml"), "rb") as f:
            return tomllib.load(f)["tool"]["poetry"]["version"]

    _version = pkg_version()
    assert _version is not None
    __version__ = _version
    del _version
