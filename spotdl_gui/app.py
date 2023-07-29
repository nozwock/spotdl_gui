import os
import sys
import time
from multiprocessing import Process
from pathlib import Path

import platformdirs
from PySide6 import QtCore
from PySide6.QtCore import QObject, QRunnable, QSize, Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from spotdl_gui.config import Config
from spotdl_gui.spotdl_api import SpotdlApi

CONFIG = Config.load()


class PollProc(QtCore.QThread):
    proc_done = Signal()

    def __init__(self, parent, proc: Process):
        super().__init__(parent)
        self.stop = False
        self.proc = proc

    def run(self):
        while not self.stop:
            if not self.proc.is_alive():
                self.proc_done.emit()
                break
            time.sleep(0.1)


class MainWindow(QMainWindow):
    CHOICES = ["Liked Songs", "All User Playlists", "Custom Query"]
    POLLPROC_THREAD: PollProc | None = None
    DOWNLOAD_PROC: Process | None = None

    def __init__(self):
        super().__init__()

        self.resize(250, 100)
        self.setWindowTitle("Spotdl GUI")

        self.menubar = self.menuBar()
        filemenu = self.menubar.addMenu("File")
        outputdir = QAction("Pick output folder", self)
        outputdir.triggered.connect(
            lambda: set_output_dir(
                QFileDialog.getExistingDirectory(
                    self,
                    "Pick output folder",
                    dir=str(CONFIG.output_dir.absolute()),
                )
            )
        )
        filemenu.addAction(outputdir)

        self.statusbar = self.statusBar()

        self.pages = QStackedLayout()

        main_page = QWidget()
        main_vbox = QVBoxLayout()
        main_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_page.setLayout(main_vbox)
        self.pages.addWidget(main_page)

        self.choice_list = QComboBox(self)
        main_vbox.addWidget(self.choice_list)
        self.choice_list.addItems(self.CHOICES)

        self.query = QLineEdit(self)
        main_vbox.addWidget(self.query)
        self.query.setPlaceholderText("Playlist link, Song link, etc...")
        self.query.setToolTip(
            r"""Spotify/YouTube URL for a song/playlist/album/artist/etc. to download.

For album/playlist/artist searching, include 'album:', 'playlist:', 'artist:'
(ie. 'album:the album name' you can mix these options to get more accurate results).
        """
        )
        self.query.setMaximumWidth(250)
        self.query.hide()
        self.choice_list.currentTextChanged.connect(
            lambda: self.query.show()
            if self.choice_list.currentText() == self.CHOICES[2]
            else self.query.hide()
        )

        download_btn = QPushButton("Download", self)
        main_vbox.addWidget(download_btn)
        download_btn.clicked.connect(self.download_btn_clicked)

        cancel_page = QWidget()
        cancel_vbox = QVBoxLayout()
        cancel_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cancel_page.setLayout(cancel_vbox)
        self.pages.addWidget(cancel_page)

        cancel_btn = QPushButton("Cancel", self)
        cancel_vbox.addWidget(cancel_btn)
        cancel_btn.clicked.connect(self.cancel_btn_clicked)

        self.pages.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(self.pages)
        self.setCentralWidget(widget)

    def closeEvent(self, event):
        self.stop_poll_proc_thread()
        self.kill_download_proc()

        CONFIG.store()

    def set_page(self, page_idx: int = 0, menubar_enabled: bool = True) -> None:
        self.pages.setCurrentIndex(page_idx)
        self.menubar.setEnabled(menubar_enabled)

    def download_btn_clicked(self) -> None:
        self.set_page(1, False)
        self.statusbar.showMessage("Downloading...")
        self.init_download()

        assert self.DOWNLOAD_PROC is not None
        poll = PollProc(self, self.DOWNLOAD_PROC)
        poll.proc_done.connect(
            self.on_proc_complete
        )  # Go back to the main page once the proc is complete
        poll.start()
        self.POLLPROC_THREAD = poll

    def cancel_btn_clicked(self) -> None:
        self.stop_poll_proc_thread()
        self.kill_download_proc()

        self.set_page()
        self.statusbar.showMessage("Process canceled", 5000)
        clear_screen()
        print("Process canceled")

    def on_proc_complete(self) -> None:
        self.set_page()
        self.statusbar.showMessage("Process complete", 5000)
        self.kill_download_proc()
        print("Process complete")

    def init_download(self) -> None:
        def _download(query: list[str]) -> None:
            api = SpotdlApi(user_auth=True)
            api.downloader.settings.update(
                {
                    "sponsor_block": True,
                    "print_errors": True,
                    "output": str(CONFIG.output_dir.absolute()),
                }
            )
            api.simple_search_and_download(query)

        choice = self.choice_list.currentText()
        query = self.query.text()

        print(f"Starting download for {choice}")

        if choice == self.CHOICES[0]:
            p = Process(target=_download, args=(["saved"],))
        elif choice == self.CHOICES[1]:
            p = Process(target=_download, args=(["all-user-playlists"],))
        elif choice == self.CHOICES[2]:
            p = Process(target=_download, args=([query],))
        else:
            raise Exception("Impossible case")

        self.DOWNLOAD_PROC = p
        p.start()

    def stop_poll_proc_thread(self):
        if self.POLLPROC_THREAD is not None:
            if self.POLLPROC_THREAD.isRunning():
                self.POLLPROC_THREAD.proc_done.disconnect(self.on_proc_complete)
                self.POLLPROC_THREAD.stop = True
            self.POLLPROC_THREAD = None

    def kill_download_proc(self) -> None:
        if self.DOWNLOAD_PROC is not None:
            if self.DOWNLOAD_PROC.is_alive():
                self.DOWNLOAD_PROC.kill()
            self.DOWNLOAD_PROC = None


def set_output_dir(dir: Path | str) -> None:
    if isinstance(dir, str):
        dir = Path(dir)

    if dir != CONFIG.output_dir:
        CONFIG.output_dir = dir
    print(f"Output folder: {dir.absolute()}")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    set_output_dir(CONFIG.output_dir)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
