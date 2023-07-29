import sys

import qdarktheme
from assets import resource
from PySide6 import QtWidgets
from views.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("SpotDL GUI")


app = QtWidgets.QApplication(sys.argv)
qdarktheme.setup_theme()

window = MainWindow()
window.show()
app.exec()
