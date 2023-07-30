# Form implementation generated from reading ui file '/home/nozwock/hub/dev/repo/spotdl_gui/spotdl_gui/views/mainwindow.ui'
#
# Created by: PySide6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(688, 483)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_search.setMinimumSize(QtCore.QSize(125, 0))
        self.lineEdit_search.setText("")
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.pushButton_search = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_search.setObjectName("pushButton_search")
        self.horizontalLayout.addWidget(self.pushButton_search)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.stackedWidget_pages = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget_pages.setObjectName("stackedWidget_pages")
        self.page_intro = QtWidgets.QWidget()
        self.page_intro.setObjectName("page_intro")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_intro)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(parent=self.page_intro)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(parent=self.page_intro)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.stackedWidget_pages.addWidget(self.page_intro)
        self.page_searching = QtWidgets.QWidget()
        self.page_searching.setObjectName("page_searching")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_searching)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.label_searching = QtWidgets.QLabel(parent=self.page_searching)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_searching.sizePolicy().hasHeightForWidth())
        self.label_searching.setSizePolicy(sizePolicy)
        self.label_searching.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_searching.setObjectName("label_searching")
        self.verticalLayout_6.addWidget(self.label_searching, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.progressBar_search = QtWidgets.QProgressBar(parent=self.page_searching)
        self.progressBar_search.setMinimumSize(QtCore.QSize(300, 0))
        self.progressBar_search.setMaximumSize(QtCore.QSize(650, 16777215))
        self.progressBar_search.setMaximum(0)
        self.progressBar_search.setProperty("value", -1)
        self.progressBar_search.setObjectName("progressBar_search")
        self.verticalLayout_6.addWidget(self.progressBar_search, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.pushButton_cancel_search = QtWidgets.QPushButton(parent=self.page_searching)
        self.pushButton_cancel_search.setMinimumSize(QtCore.QSize(300, 0))
        self.pushButton_cancel_search.setObjectName("pushButton_cancel_search")
        self.verticalLayout_6.addWidget(self.pushButton_cancel_search, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_6.addItem(spacerItem3)
        self.stackedWidget_pages.addWidget(self.page_searching)
        self.page_tracks_list = QtWidgets.QWidget()
        self.page_tracks_list.setObjectName("page_tracks_list")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_tracks_list)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView_tracks_list = QtWidgets.QTableView(parent=self.page_tracks_list)
        self.tableView_tracks_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView_tracks_list.setObjectName("tableView_tracks_list")
        self.verticalLayout.addWidget(self.tableView_tracks_list)
        self.stackedWidget_pages.addWidget(self.page_tracks_list)
        self.page_downloading = QtWidgets.QWidget()
        self.page_downloading.setObjectName("page_downloading")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_downloading)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.label_downloading = QtWidgets.QLabel(parent=self.page_downloading)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_downloading.sizePolicy().hasHeightForWidth())
        self.label_downloading.setSizePolicy(sizePolicy)
        self.label_downloading.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_downloading.setObjectName("label_downloading")
        self.verticalLayout_5.addWidget(self.label_downloading, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.progressBar_download = QtWidgets.QProgressBar(parent=self.page_downloading)
        self.progressBar_download.setMinimumSize(QtCore.QSize(300, 0))
        self.progressBar_download.setMaximum(0)
        self.progressBar_download.setProperty("value", -1)
        self.progressBar_download.setObjectName("progressBar_download")
        self.verticalLayout_5.addWidget(self.progressBar_download, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.pushButton_cancel_download = QtWidgets.QPushButton(parent=self.page_downloading)
        self.pushButton_cancel_download.setMinimumSize(QtCore.QSize(300, 0))
        self.pushButton_cancel_download.setObjectName("pushButton_cancel_download")
        self.verticalLayout_5.addWidget(self.pushButton_cancel_download, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem5)
        self.stackedWidget_pages.addWidget(self.page_downloading)
        self.verticalLayout_3.addWidget(self.stackedWidget_pages)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 688, 23))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(parent=self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(parent=self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(36, 36))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen_SpotDL_config_folder = QtGui.QAction(parent=MainWindow)
        self.actionOpen_SpotDL_config_folder.setObjectName("actionOpen_SpotDL_config_folder")
        self.actionSettings = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/bx-cog.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionSettings.setIcon(icon)
        self.actionSettings.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionSettings.setObjectName("actionSettings")
        self.actionDownload = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/bx-download.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionDownload.setIcon(icon1)
        self.actionDownload.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionDownload.setObjectName("actionDownload")
        self.actionExport = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/bxs-file-export.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExport.setIcon(icon2)
        self.actionExport.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionExport.setObjectName("actionExport")
        self.actionImport = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/bxs-file-import.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionImport.setIcon(icon3)
        self.actionImport.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionImport.setObjectName("actionImport")
        self.actionPick_Output_Folder = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/bxs-folder-open.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPick_Output_Folder.setIcon(icon4)
        self.actionPick_Output_Folder.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionPick_Output_Folder.setObjectName("actionPick_Output_Folder")
        self.actionAbout = QtGui.QAction(parent=MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionOpen_SpotDL_config_folder)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionPick_Output_Folder)
        self.toolBar.addAction(self.actionImport)
        self.toolBar.addAction(self.actionExport)
        self.toolBar.addAction(self.actionDownload)
        self.toolBar.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)
        self.stackedWidget_pages.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SpotDL GUI"))
        self.lineEdit_search.setPlaceholderText(_translate("MainWindow", "🔍  Search for tracks or paste link here..."))
        self.pushButton_search.setText(_translate("MainWindow", "Search"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:700; color:#ffb27f;\">Spotify Downloader</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/images/music-note-slider.svg\"/></p></body></html>"))
        self.label_searching.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">Processing query</span></p><p><span style=\" font-size:12pt;\">&quot;%query%&quot;</span></p></body></html>"))
        self.pushButton_cancel_search.setText(_translate("MainWindow", "Cancel"))
        self.label_downloading.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">Downloading %count% track(s)</span></p></body></html>"))
        self.pushButton_cancel_download.setText(_translate("MainWindow", "Cancel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen_SpotDL_config_folder.setText(_translate("MainWindow", "Open SpotDL Config Folder"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionDownload.setText(_translate("MainWindow", "Download"))
        self.actionDownload.setToolTip(_translate("MainWindow", "Download selected tracks"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionExport.setToolTip(_translate("MainWindow", "Export tracks list to a file"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionImport.setToolTip(_translate("MainWindow", "Import exported tracks list"))
        self.actionPick_Output_Folder.setText(_translate("MainWindow", "Pick Output Folder"))
        self.actionPick_Output_Folder.setToolTip(_translate("MainWindow", "Pick output folder"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
