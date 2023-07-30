import sys
from pathlib import Path

import qdarktheme
from PySide6 import QtWidgets
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWidgets import QDialog, QFileDialog, QWidget

from .assets import resource
from .config import Config
from .models.tracks_model import TracksModel
from .spotdl_api import Song
from .views.about import Ui_About
from .views.mainwindow import Ui_MainWindow
from .workers.search_worker import SearchWorker


class AboutDialog(QtWidgets.QDialog, Ui_About):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.setupUi(self)
        self.set_page(0)

        self.config = Config.load()

        self.threadpool = QThreadPool(self)

        self.about_dialog = AboutDialog(self)
        self.actionAbout.triggered.connect(lambda: self.about_dialog.exec())

        self.actionPick_Output_Folder.triggered.connect(
            lambda: self.set_output_dir(
                QFileDialog.getExistingDirectory(
                    self,
                    "Pick output folder",
                    dir=str(self.config.output_dir.absolute()),
                )
            )
        )

        self.tracks_model = TracksModel()
        self.tableView_tracks_list.setModel(self.tracks_model)

        self.search_kb_shortcut = QShortcut(
            QKeySequence("Return"), self.lineEdit_search, self.search
        )
        self.pushButton_search.clicked.connect(self.search)

        self.label_searching_text = self.label_searching.text()

    def closeEvent(self, event):
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
            print(f"{e}\nError")

        def cancel_search() -> None:
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
