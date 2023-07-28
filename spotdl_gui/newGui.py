import sys

import qdarktheme
from assets import resource
from PyQt6 import QtWidgets, uic
from views.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("SpotDL GUI")


app = QtWidgets.QApplication(sys.argv)
qdarktheme.setup_theme()

window = MainWindow()
window.show()
app.exec()
