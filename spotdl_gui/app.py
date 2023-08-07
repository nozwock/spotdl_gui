import dataclasses
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Iterable

import qdarktheme
from pyqtconfig import ConfigManager
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

from . import __version__
from .assets import resource  # noqa: F401
from .config import Config
from .defines import SPOTDL_FILE_FILTER, SPOTDL_VERSION
from .models.tracks_model import TracksModel
from .spotdl_api import (
    Song,
    generate_initial_config,
    get_spotdl_config,
    get_spotdl_config_path,
    get_spotdl_dir,
)
from .utils import open_default, shorten_string, with_extension
from .views.about import Ui_About
from .views.mainwindow import Ui_MainWindow
from .views.settings import Ui_Settings
from .workers.download_worker import DownloadWorker
from .workers.search_worker import SearchWorker


def detailed_dialog(
    parent: QWidget,
    title: str,
    text: str,
    /,
    icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon,
    detailed_text: str | None = None,
    *args,
    **kwargs,
) -> QMessageBox:
    msg = QMessageBox(parent, *args, **kwargs)
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(text)

    if detailed_text:
        msg.setDetailedText(detailed_text)

    return msg


class SpotdlConfigManager(ConfigManager):
    OPTIONAL_PREF_PREFIX = (
        "optionalGroup_"  # i.e. for `WidgetValue | None` depending on CheckBox state
    )

    def __init__(self, *args, optionals: Iterable[str] | None = None, **kwargs):
        super().__init__(
            *args,
            **kwargs,
        )

        self.path = get_spotdl_config_path()

        generate_initial_config()
        _spotdl_config = get_spotdl_config()
        if optionals is not None:
            self._add_optionals(_spotdl_config, optionals)

        self.set_defaults(_spotdl_config)
        self.set_many(_spotdl_config)

    def add_handlers_keyless(self, handlers: Iterable[QWidget]) -> None:
        self.add_handlers(
            dict(SpotdlConfigManager._get_handler_args(handler) for handler in handlers)
        )

    @staticmethod
    def _get_handler_args(widget: QWidget) -> tuple[str, QWidget]:
        return (
            widget.objectName().split("_", 2)[-1],
            widget,
        )  # eg. 'checkBox_downloader_print_errors' -> 'print_errors'

    def _add_optionals(self, cfg: dict[str, Any], optionals) -> None:
        cfg.update(
            {
                f"{SpotdlConfigManager.OPTIONAL_PREF_PREFIX}{pref}": False
                for pref in optionals
            }
        )

    def _resolve_optionals(self, cfg: dict[str, Any]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k in cfg:
            if k.startswith(SpotdlConfigManager.OPTIONAL_PREF_PREFIX):
                assert isinstance(cfg[k], bool)
                if cfg[k]:
                    out[k.lstrip(SpotdlConfigManager.OPTIONAL_PREF_PREFIX)] = None
            elif out.get(k) is None:
                out[k] = cfg[k]
        return out

    def as_dict(self) -> dict[str, Any]:
        return self._resolve_optionals(self.config)


class AboutDialog(QtWidgets.QDialog, Ui_About):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.label_about.setText(
            self.label_about.text()
            .replace(r"%version%", __version__)
            .replace(r"%spotdlversion%", SPOTDL_VERSION)
        )


class SettingsDialog(QtWidgets.QDialog, Ui_Settings):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        widget: QWidget
        for widget in (
            self.lineEdit_spotify_auth_token,
            self.cookie_file_group,
            self.comboBox_downloader_bitrate,
            self.lineEdit_downloader_ffmpeg_args,
            self.lineEdit_downloader_m3u,
        ):
            widget.setHidden(True)

        self.comboBox_downloader_log_level.addItems(logging._nameToLevel.keys())

        self.toolButton_cache_path_pick.clicked.connect(
            lambda: self._put_file_path_to_lineEdit(self.lineEdit_spotify_cache_path)
        )
        self.toolButton_cookie_file_pick.clicked.connect(
            lambda: self._put_file_path_to_lineEdit(
                self.lineEdit_downloader_cookie_file
            )
        )
        self.toolButton_ffmpeg_pick.clicked.connect(
            lambda: self._put_file_path_to_lineEdit(self.lineEdit_downloader_ffmpeg)
        )

        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).clicked.connect(self.accept)
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Discard
        ).clicked.connect(self.reject)

        self.setup_spotdl_config()

    def _put_file_path_to_lineEdit(self, widget: QtWidgets.QLineEdit):
        path = QFileDialog.getOpenFileName(self)[0]
        if path:
            widget.setText(path)

    @QtCore.Slot()
    def accept(self) -> None:
        # There probably is a better way...
        self.spotdl_config.set_defaults(self.spotdl_config.config)
        # TODO: Pass the config to downloader, instead of writing everytime.
        # And save only once on exit.
        self.spotdl_config.save()
        super().accept()

    @QtCore.Slot()
    def reject(self) -> None:
        self.spotdl_config.set_many(self.spotdl_config.defaults)
        super().reject()

    def setup_spotdl_config(self) -> None:
        self.spotdl_config = SpotdlConfigManager(
            optionals=("auth_token", "cookie_file", "bitrate", "ffmpeg_args", "m3u")
        )

        # Adding widget handlers
        self.spotdl_config.add_handlers_keyless(
            (
                # Spotify handlers
                self.lineEdit_spotify_client_id,
                self.lineEdit_spotify_client_secret,
                self.checkBox_spotify_optionalGroup_auth_token,
                self.lineEdit_spotify_auth_token,
                self.checkBox_spotify_user_auth,
                self.checkBox_spotify_headless,
                self.lineEdit_spotify_cache_path,
                self.checkBox_spotify_no_cache,
                self.checkBox_spotify_use_cache_file,
                self.spinBox_spotify_max_retries,
                # Downloader handlers
                self.checkBox_downloader_optionalGroup_bitrate,
                self.comboBox_downloader_bitrate,
                self.comboBox_downloader_format,
                self.spinBox_downloader_threads,
                self.checkBox_downloader_optionalGroup_cookie_file,
                self.lineEdit_downloader_cookie_file,
                self.checkBox_downloader_sponsorblock,
                self.checkBox_downloader_print_errors,
                self.checkBox_downloader_playlist_numbering,
                self.checkBox_downloader_scan_for_songs,
                self.checkBox_downloader_optionalGroup_m3u,
                self.lineEdit_downloader_m3u,
                self.comboBox_downloader_overwrite,
                self.lineEdit_downloader_output,
                self.comboBox_downloader_log_level,
                self.lineEdit_downloader_ffmpeg,
                self.lineEdit_downloader_ffmpeg_args,
                self.checkBox_downloader_optionalGroup_ffmpeg_args,
            )
        )


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"{self.windowTitle()} v{__version__}")
        self.set_page(0)

        # Setup dialogs
        self.about_dialog = AboutDialog(self)
        self.actionAbout.triggered.connect(lambda: self.about_dialog.exec())

        self.settings_dialog = SettingsDialog(self)
        self.actionSettings.triggered.connect(lambda: self.settings_dialog.exec())

        # Load app config
        self.config = Config.load()

        # Initials text for substitution
        self.label_searching_text = self.label_searching.text()
        self.label_downloading_text = self.label_downloading.text()

        # Search bar
        self.search_completer = QtWidgets.QCompleter(
            (
                "user:saved-tracks",
                "user:all-playlists",
                "album:",
                "playlist:",
                "artist:",
            ),
            self,
        )
        self.lineEdit_search.setCompleter(self.search_completer)

        # Setup tracks list model
        self.tracks_model = TracksModel()
        self.tableView_tracks_list.setModel(self.tracks_model)

        # Setup status bar
        self.label_statusbar_output_dir = QtWidgets.QLabel("")
        self.label_statusbar_output_dir.mousePressEvent = lambda *_: open_default(  # type: ignore[method-assign]
            self.config.output_dir
        )
        self.statusbar.addWidget(self.label_statusbar_output_dir)
        self.set_output_dir(self.config.output_dir)

        # Workers
        self.threadpool = QThreadPool(self)
        self.search_worker: SearchWorker | None = None
        self.download_worker: DownloadWorker | None = None

        # Setup actions
        self.actionOpen_spotDL_config_folder.triggered.connect(
            lambda: open_default(get_spotdl_dir())
        )

        self.actionPick_Output_Folder.triggered.connect(
            lambda: self.set_output_dir(
                QFileDialog.getExistingDirectory(
                    self,
                    self.actionPick_Output_Folder.toolTip(),
                    dir=str(
                        self.config.output_dir.absolute()
                        if self.config.output_dir.is_dir()
                        else Path()
                    ),
                )
            )
        )

        # self.search_kb_shortcut = QShortcut(
        #     QKeySequence("Ctrl+Return"), self.lineEdit_search, self.search
        # )
        self.pushButton_search.clicked.connect(self.search)

        self.actionImport.triggered.connect(self.import_tracks_from_file)
        self.actionExport.triggered.connect(self.export_tracks_to_file)
        self.actionDownload.triggered.connect(self.download)

    def closeEvent(self, event):
        if self.search_worker:
            self.search_worker.kill()
        if self.download_worker:
            self.download_worker.kill()

        self.threadpool.clear()

        self.config.store()

    def set_page(self, idx: int) -> None:
        def reset_progressbar() -> None:
            self.progressBar_download.setMaximum(0)
            self.progressBar_download.setValue(-1)

        def hide_search_bar(yes: bool) -> None:
            if yes:
                self.lineEdit_search.hide()
                self.pushButton_search.hide()
            else:
                self.lineEdit_search.show()
                self.pushButton_search.show()

        self.stackedWidget_pages.setCurrentIndex(idx)
        if idx == 0:
            self.actionDownload.setDisabled(True)
            self.actionExport.setDisabled(True)
            self.actionImport.setDisabled(False)
            hide_search_bar(False)
            reset_progressbar()
        elif idx == 1:
            self.actionDownload.setDisabled(True)
            self.actionExport.setDisabled(True)
            self.actionImport.setDisabled(True)
            hide_search_bar(True)
        elif idx == 2:
            self.actionDownload.setDisabled(False)
            self.actionExport.setDisabled(False)
            self.actionImport.setDisabled(False)
            hide_search_bar(False)
            reset_progressbar()
        elif idx == 3:
            self.actionDownload.setDisabled(True)
            self.actionExport.setDisabled(True)
            self.actionImport.setDisabled(True)
            hide_search_bar(True)
        else:
            raise Exception

    def search(self) -> None:
        def search_success(v) -> None:
            self.tracks_model.tracks = v
            self.tracks_model.layoutChanged.emit()
            self.set_page(2)

        def search_error(err: tuple[Exception, str]) -> None:
            exc, trace = err

            self.set_page(0)
            detailed_dialog(
                self,
                "Search failed",
                repr(exc),
                icon=QMessageBox.Icon.Critical,
                detailed_text=trace,
            ).exec()

        def cancel_search() -> None:
            if self.search_worker:
                self.search_worker.kill()
                self.set_page(0)

        self.label_searching.setText(
            self.label_searching_text.replace(
                "%query%", shorten_string(self.lineEdit_search.text())
            )
        )
        self.set_page(1)

        self.search_worker = SearchWorker(query=self.lineEdit_search.text())
        self.search_worker.signals.result.connect(search_success)
        self.search_worker.signals.error.connect(search_error)
        self.pushButton_cancel_search.clicked.connect(cancel_search)
        self.threadpool.start(self.search_worker)

    def download(self) -> None:
        def download_success(res: tuple[list[Any], str]) -> None:
            tracks, log_path = res
            with open(log_path, "r") as f:
                logs = f.read()

            self.set_page(2)
            detailed_dialog(
                self,
                "Download complete",
                f"Downloaded {len(tracks)} track(s) in {self.config.output_dir}",
                icon=QMessageBox.Icon.Information,
                detailed_text=logs,
            ).exec()

            os.remove(log_path)

        def download_error(err: tuple[Exception, str]) -> None:
            exc, trace = err

            self.set_page(2)
            detailed_dialog(
                self,
                "Download failed",
                repr(exc),
                icon=QMessageBox.Icon.Critical,
                detailed_text=trace,
            ).exec()

        def cancel_download() -> None:
            if self.download_worker:
                self.download_worker.kill()
                self.set_page(2)

        def handle_progress(pinfo: tuple[float, int]) -> None:
            progress, total = pinfo
            if progress > 0:
                if self.progressBar_download.maximum() == 0:
                    self.progressBar_download.setMaximum(total)
                self.progressBar_download.setValue(int(progress))

        songs = [
            self.tracks_model.tracks[row.row()]
            for row in self.tableView_tracks_list.selectionModel().selectedRows()
        ]

        if songs:
            self.set_page(3)
            self.label_downloading.setText(
                self.label_downloading_text.replace("%count%", str(len(songs)))
            )

            log_level = logging._nameToLevel.get(
                self.settings_dialog.spotdl_config.get("log_level")
            )
            log_level = log_level if log_level else logging.DEBUG

            self.download_worker = DownloadWorker(
                songs, self.config.output_dir, log_level
            )
            self.download_worker.signals.result.connect(download_success)
            self.download_worker.signals.error.connect(download_error)
            self.download_worker.signals.progress.connect(handle_progress)
            self.pushButton_cancel_download.clicked.connect(cancel_download)
            self.threadpool.start(self.download_worker)
        else:
            QMessageBox.information(
                self, "No tracks selected", "Only selected tracks will be downloaded"
            )

    def import_tracks_from_file(self) -> None:
        import_file = (
            QFileDialog.getOpenFileName(  # TODO: Have the filter be case insensitive
                self, self.actionImport.toolTip(), filter=SPOTDL_FILE_FILTER
            )[0]
        )

        if not import_file:
            return

        try:
            with open(import_file, "r", encoding="utf-8") as f:
                self.tracks_model.tracks = [Song(**song) for song in json.load(f)]
                self.tracks_model.layoutChanged.emit()
                self.set_page(2)
        except Exception as e:
            QMessageBox.critical(self, "Import failed", repr(e))

    def export_tracks_to_file(self) -> None:
        export_file_ = QFileDialog.getSaveFileName(
            self, self.actionExport.toolTip(), filter=SPOTDL_FILE_FILTER
        )[0]

        if not export_file_:
            return

        export_file = with_extension(Path(export_file_), ".spotdl")

        try:
            with open(export_file, "w", encoding="utf-8") as f:
                json.dump(
                    [dataclasses.asdict(song) for song in self.tracks_model.tracks],
                    f,
                    indent=4,
                    ensure_ascii=False,
                )
        except Exception as e:
            QMessageBox.critical(self, "Export failed", repr(e))
        QMessageBox.information(
            self,
            "Export complete",
            f"Exported {len(self.tracks_model.tracks)} track(s) to {export_file}",
        )

    def get_output_dir_label(self) -> str:
        return f"Download folder: {shorten_string(str(self.config.output_dir), width=50, lshorten=True)}"

    def set_output_dir(self, dir: Path | str) -> None:
        if isinstance(dir, str):
            if not dir:
                return None
            dir = Path(dir)

        if not dir.is_dir():
            dir = Path()

        self.config.output_dir = dir.absolute()
        self.label_statusbar_output_dir.setText(self.get_output_dir_label())


def main() -> None:
    from multiprocessing import freeze_support

    freeze_support()

    import os

    from .utils import is_frozen

    # Close pyinstaller splash window
    is_splash_enabled = os.environ.get("_PYIBoot_SPLASH")
    if is_frozen and is_splash_enabled:
        import pyi_splash

        if pyi_splash.is_alive():
            pyi_splash.close()

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/images/music-note-slider.svg"))
    qdarktheme.setup_theme()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
