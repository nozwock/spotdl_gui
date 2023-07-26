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
TODO disable menu in cancel page
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(250, 100)
        self.setMaximumSize(QSize(270, 100))
        self.setWindowTitle("Spotdl GUI")

        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        outputdir = QAction("Pick output folder", self)
        outputdir.triggered.connect(
            lambda: set_output_dir(
                QFileDialog.getExistingDirectory(self, "Pick output folder")
            )
        )
        filemenu.addAction(outputdir)

        pages = QStackedLayout()

        main_page = QWidget()
        main_vbox = QVBoxLayout()
        main_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_page.setLayout(main_vbox)
        pages.addWidget(main_page)

        choice_list = QComboBox(self)
        main_vbox.addWidget(choice_list)
        choice_list.addItems(CHOICES)

        sync_btn = QPushButton("Sync / Download", self)
        main_vbox.addWidget(sync_btn)
        sync_btn.clicked.connect(
            lambda: sync_btn_clicked(pages, 1, choice_list.currentText())
        )

        cancel_page = QWidget()
        cancel_vbox = QVBoxLayout()
        cancel_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cancel_page.setLayout(cancel_vbox)
        pages.addWidget(cancel_page)

        cancel_btn = QPushButton("Cancel", self)
        cancel_vbox.addWidget(cancel_btn)
        cancel_btn.clicked.connect(lambda: cancel_btn_clicked(pages, 0))

        pages.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(pages)
        self.setCentralWidget(widget)

    def closeEvent(self, event):
        kill_all_procs()


def kill_all_procs() -> None:
    for p in PROCS:
        p.kill()
        PROCS.pop(0)


def sync_btn_clicked(pages: QStackedLayout, page_idx: int, choice: str) -> None:
    pages.setCurrentIndex(page_idx)
    init_sync(choice)


def cancel_btn_clicked(pages: QStackedLayout, page_idx: int) -> None:
    kill_all_procs()
    pages.setCurrentIndex(page_idx)
    print("Sync canceled")


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
