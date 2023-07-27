import os
import pickle
import subprocess
import sys
import time
from multiprocessing import Process
from pathlib import Path

import platformdirs
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from spotdl_gui.spotdl_api import SpotdlApi

CHOICES = ["Liked Songs", "All User Playlists", "Custom Query"]
PROCS: list[Process] = []

STATE_DIR = Path(platformdirs.user_config_dir()).joinpath("spotdl_gui")
STATE_DIR.mkdir(parents=True, exist_ok=True)
STATE_PATH = STATE_DIR.joinpath("state.pickle")

if STATE_PATH.is_file():
    with open(STATE_PATH, "rb") as f:
        STATE = pickle.load(f)
else:
    STATE = {"output_dir": Path()}


spotify_options, downloader_options = SpotdlApi.get_config_options()

spotify_options.update({"user_auth": True})
downloader_options.update({"sponsor_block": True, "print_errors": True})


class PollProc(QtCore.QThread):
    tx = QtCore.pyqtSignal(object)  # Why object? https://stackoverflow.com/a/46694063

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        while ...:
            is_procs_complete = all(not p.is_alive() for p in PROCS)
            if is_procs_complete:
                kill_all_procs()
                self.tx.emit(0)
                break
            time.sleep(0.1)
        self.exit()


class MainWindow(QMainWindow):
    threads: list[QtCore.QThread] = []

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
                    directory=str(STATE["output_dir"].absolute()),
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
        self.choice_list.addItems(CHOICES)

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
            if self.choice_list.currentText() == CHOICES[2]
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
        kill_all_procs()

        # Cleaning up threads
        for t in self.threads:
            t.disconnect()
            while t.isRunning():
                t.wait()
            self.threads.pop(0)

        with open(STATE_PATH, "wb") as f:
            pickle.dump(STATE, f)

    def set_page(self, page_idx: int = 0, menubar_enabled: bool = True) -> None:
        self.pages.setCurrentIndex(page_idx)
        self.menubar.setEnabled(menubar_enabled)

    def download_btn_clicked(self) -> None:
        self.set_page(1, False)
        self.statusbar.showMessage("Downloading...")
        init_download(self.choice_list.currentText(), self.query.text())

        poll = PollProc(self)
        poll.tx.connect(
            self.on_proc_complete
        )  # Go back to the main page once the proc is complete
        poll.start()
        self.threads.append(poll)

    def cancel_btn_clicked(self) -> None:
        kill_all_procs()

        self.threads[0].disconnect()
        self.threads.pop(0)

        self.set_page()
        self.statusbar.showMessage("Process canceled", 5000)
        clear_screen()
        print("Download canceled")

    def on_proc_complete(self) -> None:
        self.set_page()
        self.statusbar.showMessage("Process complete", 5000)
        kill_all_procs()
        print("Download complete")


def init_download(choice: str, query: str) -> None:
    def _download(query: list[str]) -> None:
        with SpotdlApi(spotify_options, downloader_options) as api:
            api.download(query)

    print(f"Starting download for {choice}")

    if choice == CHOICES[0]:
        p = Process(target=_download, args=(["saved"],))
    elif choice == CHOICES[1]:
        p = Process(target=_download, args=(["all-user-playlists"],))
    elif choice == CHOICES[2]:
        p = Process(target=_download, args=([query],))
    else:
        raise Exception("Impossible case")

    PROCS.append(p)
    p.start()


def kill_all_procs() -> None:
    for p in PROCS:
        if p.is_alive():
            p.kill()  # bcz spotdl doesn't exit after TERM, for way too long
        PROCS.pop(0)


def set_output_dir(dir: str) -> None:
    if dir:
        path = Path(dir)
        downloader_options["output"] = str(path.absolute())
        STATE["output_dir"] = path
        print(f"Output folder: {path.absolute()}")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    set_output_dir(STATE["output_dir"])
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
