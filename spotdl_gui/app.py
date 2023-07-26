import os
import subprocess
import sys
from pathlib import Path

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

"""
TODO return to main page after the process completes (polling)
"""


class MainWindow(QMainWindow):
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
                QFileDialog.getExistingDirectory(self, "Pick output folder")
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

    def sync_btn_clicked(self) -> None:
        self.pages.setCurrentIndex(1)
        self.menubar.setDisabled(True)
        init_sync(self.choice_list.currentText())

    def cancel_btn_clicked(self) -> None:
        kill_all_procs()
        self.pages.setCurrentIndex(0)
        self.menubar.setDisabled(False)
        print("Sync canceled")


def kill_all_procs() -> None:
    for p in PROCS:
        p.kill()
        PROCS.pop(0)


def init_sync(choice: str) -> None:
    print(f"Starting sync/download for {choice}")
    if choice == CHOICES[0]:
        PROCS.append(subprocess.Popen(["spotdl", "saved", "--user-auth"]))
    else:
        PROCS.append(subprocess.Popen(["spotdl", "all-user-playlists", "--user-auth"]))


def set_output_dir(dir: str) -> None:
    if dir:
        path = Path(dir)
        os.chdir(path)
        print(f"Output folder: {path.absolute()}")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
