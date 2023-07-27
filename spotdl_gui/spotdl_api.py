import os
import sys
from typing import Any

import spotdl
from spotdl.download.downloader import Downloader
from spotdl.types.options import DownloaderOptions, SpotifyOptions
from spotdl.utils.config import DOWNLOADER_OPTIONS, SPOTIFY_OPTIONS, get_config
from spotdl.utils.console import generate_initial_config
from spotdl.utils.ffmpeg import FFmpegError, is_ffmpeg_installed
from spotdl.utils.spotify import SpotifyClient, SpotifyError, save_spotify_cache


class SpotdlApi:
    """WIP"""

    def __init__(
        self, spotify_options: SpotifyOptions, downloader_options: DownloaderOptions
    ):
        self.spotify_options, self.downloader_options = (
            spotify_options,
            downloader_options,
        )

        SpotifyClient.init(**self.spotify_options)
        self.spotify_client = SpotifyClient()

        self.downloader = Downloader(downloader_options)

    def download(self, query: list[str]) -> None:
        try:
            spotdl.console.download.download(query, self.downloader)
        except Exception as e:
            self._handle_err()
            raise e

    def sync(self, query: list[str]) -> None:
        try:
            spotdl.console.sync.sync(query, self.downloader)
        except Exception as e:
            self._handle_err()
            raise e

    def save(self, query: list[str]) -> None:
        try:
            self.is_user_auth()
            spotdl.console.save.save(query, self.downloader)
        except Exception as e:
            self._handle_err()
            raise e

    def meta(self, query: list[str]) -> None:
        try:
            spotdl.console.meta.meta(query, self.downloader)
        except Exception as e:
            self._handle_err()
            raise e

    def url(self, query: list[str]) -> None:
        try:
            spotdl.console.url.url(query, self.downloader)
        except Exception as e:
            self._handle_err()
            raise e

    def cleanup(self) -> None:
        if self.spotify_options["use_cache_file"]:
            save_spotify_cache(self.spotify_client.cache)
        self.downloader.progress_handler.close()

    def _handle_err(self) -> None:
        self.downloader.progress_handler.close()

    def is_user_auth(self) -> None:
        if not self.spotify_options["user_auth"]:
            raise SpotifyError("'user_auth' option wasn't set")

    def check_ffmpeg(self) -> None:
        if not is_ffmpeg_installed(self.downloader_options["ffmpeg"]):
            raise FFmpegError(
                "FFmpeg is not installed. Please run `spotdl --download-ffmpeg` to install it, "
                "or `spotdl --ffmpeg /path/to/ffmpeg` to specify the path to ffmpeg."
            )

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

    def __enter__(self):
        self.check_ffmpeg()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.cleanup()


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

    spotify_options, downloader_options = SpotdlApi.get_config_options()

    spotify_options.update({"user_auth": True})
    downloader_options.update({"sponsor_block": True, "print_errors": True})

    tempdir = tempfile.mkdtemp()
    print(f"Output folder: {tempdir}")

    downloader_options["output"] = tempdir

    with SpotdlApi(spotify_options, downloader_options) as api:
        api.download(["saved"])
