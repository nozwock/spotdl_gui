import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Iterable

import qdarktheme
from pyqtconfig import ConfigManager
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox, QTableView, QWidget

from . import __version__
from .assets import resource
from .config import Config
from .defines import SPOTDL_FILE_FILTER, SPOTDL_VERSION
from .models.tracks_model import TracksModel
from .spotdl_api import Song, get_spotdl_config, get_spotdl_path
from .utils import open_default
from .views.about import Ui_About
from .views.mainwindow import Ui_MainWindow
from .views.settings import Ui_Settings
from .workers.download_worker import DownloadWorker
from .workers.search_worker import SearchWorker

OPTIONAL_PREF_PREFIX = (
    "optionalGroup_"  # i.e. for `WidgetValue | None` depending on CheckBox state
)


class SpotdlConfigManager(ConfigManager):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self._config = get_spotdl_config()
        self._add_optionals(
            self._config, ("auth_token", "cookie_file", "bitrate", "ffmpeg_args")
        )

    def add_handlers_keyless(self, handlers: Iterable[QWidget]) -> None:
        self.add_handlers(
            dict(SpotdlConfigManager._get_handler_args(handler) for handler in handlers)
        )

    @staticmethod
    def _get_handler_args(widget: QWidget) -> tuple[str, QWidget]:
        return (widget.objectName().split("_", 2)[-1], widget)

    def _add_optionals(self, cfg: dict[str, Any], optionals) -> None:
        cfg.update({f"{OPTIONAL_PREF_PREFIX}{pref}": False for pref in optionals})

    def get_config(self) -> dict[str, Any]:
        # return after eval and removing optionals
        raise NotImplementedError
        return self._config


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

        self.lineEdit_spotify_auth_token.setHidden(True)
        self.comboBox_downloader_bitrate.setHidden(True)
        self.cookie_file_group.setHidden(True)
        self.lineEdit_downloader_ffmpeg_args.setHidden(True)

        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).clicked.connect(self.accept)
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Discard
        ).clicked.connect(self.reject)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.setupUi(self)
        self.set_page(0)

        self.about_dialog = AboutDialog(self)
        self.actionAbout.triggered.connect(lambda: self.about_dialog.exec())

        self.settings_dialog = SettingsDialog(self)
        self.actionSettings.triggered.connect(lambda: self.settings_dialog.exec())

        self.config = Config.load()
        self.setup_spotdl_config()

        self.label_searching_text = self.label_searching.text()
        self.label_downloading_text = self.label_downloading.text()

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

        self.threadpool = QThreadPool(self)
        self.search_worker: SearchWorker | None = None
        self.download_worker: DownloadWorker | None = None

        self.actionOpen_SpotDL_config_folder.triggered.connect(
            lambda: open_default(get_spotdl_path())
        )

        self.actionPick_Output_Folder.triggered.connect(
            lambda: self.set_output_dir(
                QFileDialog.getExistingDirectory(
                    self,
                    "Pick output folder",
                    dir=str(
                        self.config.output_dir.absolute()
                        if self.config.output_dir.is_dir()
                        else Path()
                    ),
                )
            )
        )

        self.tracks_model = TracksModel()
        self.tableView_tracks_list.setModel(self.tracks_model)

        # self.search_kb_shortcut = QShortcut(
        #     QKeySequence("Ctrl+Return"), self.lineEdit_search, self.search
        # )
        self.pushButton_search.clicked.connect(self.search)

        self.actionImport.triggered.connect(self.import_tracks_from_file)
        self.actionExport.triggered.connect(self.export_tracks_to_file)
        self.actionDownload.triggered.connect(self.download)

    def setup_spotdl_config(self) -> None:
        self.spotdl_config_manager = SpotdlConfigManager()

        # Adding widget handlers
        s = self.settings_dialog
        self.spotdl_config_manager.add_handlers_keyless(
            (
                # Spotify handlers
                s.lineEdit_spotify_client_id,
                s.lineEdit_spotify_client_secret,
                s.checkBox_spotify_optionalGroup_auth_token,
                s.lineEdit_spotify_auth_token,
                s.checkBox_spotify_user_auth,
                s.checkBox_spotify_headless,
                s.lineEdit_spotify_cache_path,
                s.checkBox_spotify_no_cache,
                s.checkBox_spotify_use_cache_file,
                s.spinBox_spotify_max_retries,
                # Downloader handlers
                s.checkBox_downloader_optionalGroup_bitrate,
                s.comboBox_downloader_bitrate,
                s.comboBox_downloader_format,
                s.spinBox_downloader_threads,
                s.checkBox_downloader_optionalGroup_cookie_file,
                s.lineEdit_downloader_cookie_file,
                s.checkBox_downloader_sponsorblock,
                s.checkBox_downloader_print_errors,
                s.checkBox_downloader_playlist_numbering,
                s.checkBox_downloader_scan_for_songs,
                s.comboBox_downloader_overwrite,
                s.lineEdit_downloader_output,
                s.lineEdit_downloader_ffmpeg,
                s.lineEdit_downloader_ffmpeg_args,
                s.checkBox_downloader_optionalGroup_ffmpeg_args,
            )
        )

    def closeEvent(self, event):
        if self.search_worker:
            self.search_worker.kill()
        if self.download_worker:
            self.download_worker.kill()

        self.threadpool.clear()

        self.config.store()

    def set_page(self, idx: int) -> None:
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

        def search_error(e) -> None:
            self.set_page(0)
            QMessageBox.critical(self, "Search failed", repr(e))

        def cancel_search() -> None:
            if self.search_worker:
                self.search_worker.kill()
                self.set_page(0)

        self.set_page(1)
        self.label_searching.setText(
            self.label_searching_text.replace("%query%", self.lineEdit_search.text())
        )

        self.search_worker = SearchWorker([self.lineEdit_search.text()])
        self.search_worker.signals.result.connect(search_success)
        self.search_worker.signals.error.connect(search_error)
        self.pushButton_cancel_search.clicked.connect(cancel_search)
        self.threadpool.start(self.search_worker)

    def download(self) -> None:
        def download_success(v) -> None:
            self.set_page(2)
            QMessageBox.information(
                self,
                "Download complete",
                f"Downloaded {len(v)} track(s) in {self.config.output_dir}",
            )

        def download_error(e) -> None:
            self.set_page(2)
            QMessageBox.critical(self, "Download failed", repr(e))

        def cancel_download() -> None:
            if self.download_worker:
                self.download_worker.kill()
                self.set_page(2)

        songs = [
            self.tracks_model.tracks[row.row()]
            for row in self.tableView_tracks_list.selectionModel().selectedRows()
        ]

        if songs:
            self.set_page(3)
            self.label_downloading.setText(
                self.label_downloading_text.replace("%count%", str(len(songs)))
            )

            self.download_worker = DownloadWorker(songs, self.config.output_dir)
            self.download_worker.signals.result.connect(download_success)
            self.download_worker.signals.error.connect(download_error)
            self.pushButton_cancel_download.clicked.connect(cancel_download)
            self.threadpool.start(self.download_worker)

    def import_tracks_from_file(self) -> None:
        import_file = QFileDialog.getOpenFileName(
            self, "Import tracks from spotdl file", filter=SPOTDL_FILE_FILTER
        )[0]

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
            self, "Export tracks to spotdl file", filter=SPOTDL_FILE_FILTER
        )[0]

        if not export_file_:
            return

        export_file = Path(export_file_)

        if not export_file.suffix:
            export_file = export_file.with_suffix(".spotdl")

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

    def set_output_dir(self, dir: Path | str) -> None:
        if isinstance(dir, str):
            if not dir:
                return None
            dir = Path(dir)

        if dir != self.config.output_dir:
            self.config.output_dir = dir


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
