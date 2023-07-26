import os
import pickle
import subprocess
import sys
import time
from pathlib import Path

import platformdirs
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

CHOICES = ["Liked Songs", "All User Playlists"]
PROCS: list[subprocess.Popen] = []

STATE_DIR = Path(platformdirs.user_config_dir()).joinpath("spotdl_gui")
STATE_DIR.mkdir(parents=True, exist_ok=True)
STATE_PATH = STATE_DIR.joinpath("state.pickle")

if STATE_PATH.is_file():
    with open(STATE_PATH, "rb") as f:
        STATE = pickle.load(f)
else:
    STATE = {"output_dir": Path()}


class PollProc(QtCore.QThread):
    tx = QtCore.pyqtSignal(object)  # Why object? https://stackoverflow.com/a/46694063

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        while ...:
            is_procs_complete = all(p.poll() is not None for p in PROCS)
            if is_procs_complete:
                self.tx.emit(0)
                break
            time.sleep(0.1)
        self.exit()


class MainWindow(QMainWindow):
    threads: list[QtCore.QThread] = []

    def __init__(self):
        super().__init__()

        self.resize(250, 100)
        self.setMaximumSize(QSize(270, 100))
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

        self.pages = QStackedLayout()

        main_page = QWidget()
        main_vbox = QVBoxLayout()
        main_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_page.setLayout(main_vbox)
        self.pages.addWidget(main_page)

        self.choice_list = QComboBox(self)
        main_vbox.addWidget(self.choice_list)
        self.choice_list.addItems(CHOICES)

        sync_btn = QPushButton("Sync / Download", self)
        main_vbox.addWidget(sync_btn)
        sync_btn.clicked.connect(self.sync_btn_clicked)

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

    def sync_btn_clicked(self) -> None:
        self.set_page(1, False)
        init_sync(self.choice_list.currentText())

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
        clear_screen()
        print("Sync canceled")

    def on_proc_complete(self):
        self.set_page()
        kill_all_procs()
        print("Sync complete")


def kill_all_procs() -> None:
    for p in PROCS:
        if p.poll() is None:
            p.kill()  # bcz spotdl doesn't exit after TERM, for way too long
        PROCS.pop(0)


def init_sync(choice: str) -> None:
    print(f"Starting sync/download for {choice}")
    if choice == CHOICES[0]:
        PROCS.append(
            subprocess.Popen(["python", "-m", "spotdl", "saved", "--user-auth"])
        )
    else:
        PROCS.append(
            subprocess.Popen(
                ["python", "-m", "spotdl", "all-user-playlists", "--user-auth"]
            )
        )


def set_output_dir(dir: str) -> None:
    if dir:
        path = Path(dir)
        os.chdir(path)
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
