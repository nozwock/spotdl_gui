import sys

import qdarktheme
from assets import resource
from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog, QWidget
from views.about import Ui_About
from views.mainwindow import Ui_MainWindow


class AboutDialog(QtWidgets.QDialog, Ui_About):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.about_dialog = AboutDialog(self)
        self.actionAbout.triggered.connect(lambda: self.about_dialog.exec())


def main():
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme()

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
