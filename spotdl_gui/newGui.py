import sys

import qdarktheme
from assets import resource
from PySide6 import QtWidgets
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QDialog, QWidget
from views.about import Ui_About
from views.mainwindow import Ui_MainWindow
from workers.search_worker import SearchWorker


class AboutDialog(QtWidgets.QDialog, Ui_About):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.set_page(0)

        self.about_dialog = AboutDialog(self)
        self.actionAbout.triggered.connect(lambda: self.about_dialog.exec())

        self.threadpool = QThreadPool(self)

        self.pushButton_search.clicked.connect(self.search)

        self.label_searching_text = self.label_searching.text()

    def set_page(self, idx: int):
        def hide_search_bar(yes: bool):
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

    def search(self):
        def search_success(v):
            self.set_page(2)
            print(f"{v}\nSuccess", type(v))

        def search_error(e):
            self.set_page(0)
            print(f"{e}\nError")

        def cancel_search():
            self.search_worker.kill()
            self.set_page(0)

        self.set_page(1)
        self.label_searching.setText(
            self.label_searching_text.replace("%query%", self.lineEdit_search.text())
        )

        self.search_worker = SearchWorker(self.lineEdit_search.text())
        self.search_worker.signals.success.connect(search_success)
        self.search_worker.signals.error.connect(search_error)
        self.pushButton_cancel_search.clicked.connect(cancel_search)
        self.threadpool.start(self.search_worker)


def main():
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme()

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
