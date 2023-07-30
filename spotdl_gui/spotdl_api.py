from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import spotdl
from spotdl.download.downloader import Downloader
from spotdl.types.options import DownloaderOptions, SpotifyOptions
from spotdl.types.song import Song
from spotdl.utils.config import DOWNLOADER_OPTIONS, SPOTIFY_OPTIONS, get_config
from spotdl.utils.console import generate_initial_config
from spotdl.utils.ffmpeg import FFmpegError, is_ffmpeg_installed
from spotdl.utils.search import get_simple_songs
from spotdl.utils.spotify import SpotifyClient, SpotifyError, save_spotify_cache


class SpotdlApi(spotdl.Spotdl):
    """
    Singleton Object, arguments passed will only take effect for the first initialization.
    A wrapper over Spotdl.

    ```python
    api = SpotdlApi(user_auth=True)
    api.downloader.settings.update({"sponsor_block": True})
    api.simple_search_and_download(["saved"])
    ```
    """

    _instance: SpotdlApi | None = None

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        user_auth: bool | None = None,
        cache_path: str | None = None,
        no_cache: bool | None = None,
        headless: bool | None = None,
        downloader_options: DownloaderOptions | None = None,
    ):
        """
        Dummy method for LSP functionalities.
        """
        ...

    def __new__(
        cls,
        client_id: str | None = None,
        client_secret: str | None = None,
        user_auth: bool | None = None,
        cache_path: str | None = None,
        no_cache: bool | None = None,
        headless: bool | None = None,
        downloader_options: DownloaderOptions | None = None,
    ):
        if cls._instance is None:
            spotify_options, cfg_downloader_options = cls.get_config_options()

            if client_id is not None:
                spotify_options["client_id"] = client_id
            if client_secret is not None:
                spotify_options["client_secret"] = client_secret
            if user_auth is not None:
                spotify_options["user_auth"] = user_auth
            if cache_path is not None:
                spotify_options["client_secret"] = cache_path
            if no_cache is not None:
                spotify_options["no_cache"] = no_cache
            if headless is not None:
                spotify_options["headless"] = headless

            downloader_options = (
                cfg_downloader_options
                if downloader_options is None
                else downloader_options
            )

            cls._spotify_options = spotify_options

            SpotifyClient.init(**cls._spotify_options)
            cls._spotify_client = SpotifyClient()

            cls.downloader = Downloader(downloader_options)

            cls._instance = super().__new__(cls)

            return cls._instance
        else:
            return cls._instance

    def simple_search(self, query: list[str]) -> list[Song]:
        return get_simple_songs(
            query,
            self.downloader.settings["ytm_data"],
            self.downloader.settings["playlist_numbering"],
        )

    def simple_search_and_download(
        self, query: list[str]
    ) -> list[tuple[Song, Path | None]]:
        return self.download_songs(self.simple_search(query))

    def search_and_download(self, query: list[str]) -> list[tuple[Song, Path | None]]:
        return self.download_songs(self.search(query))

    def save_if_use_cache_file(self) -> None:
        """Save Spotify cache."""

        if self._spotify_options["use_cache_file"]:
            save_spotify_cache(self._spotify_client.cache)

    @staticmethod
    def get_config_options() -> tuple[SpotifyOptions, DownloaderOptions]:
        """
        Returns typed options from the config file.
        """

        # Make sure config exists
        generate_initial_config()

        config = get_config()

        return (
            SpotifyOptions(merge_maps(SPOTIFY_OPTIONS, config)),
            DownloaderOptions(merge_maps(DOWNLOADER_OPTIONS, config)),
        )


def merge_maps(key_from: dict[str, Any], values_from: dict[str, Any]) -> dict[str, Any]:
    """
    Returns a map identical in structure to `keys_from` but using the values from `values_from`.
    """

    out = {}
    override_keys = values_from.keys()
    for k in key_from.keys():
        if k in override_keys:
            out[k] = values_from[k]

    return out


if __name__ == "__main__":
    # Example usage
    # =============

    import tempfile

    tempdir = tempfile.mkdtemp()
    print(f"Output folder: {tempdir}")

    api = SpotdlApi(user_auth=True)
    api.downloader.settings.update({"sponsor_block": True, "output": tempdir})
    result = api.simple_search_and_download(["saved"])
    print(result)
