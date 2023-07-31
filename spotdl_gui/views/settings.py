# Form implementation generated from reading ui file '/home/nozwock/hub/dev/repo/spotdl_gui/spotdl_gui/views/settings.ui'
#
# Created by: PySide6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(400, 500)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Settings)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(parent=Settings)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -447, 366, 895))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_spotify_settings = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents)
        self.groupBox_spotify_settings.setObjectName("groupBox_spotify_settings")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_spotify_settings)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=self.groupBox_spotify_settings)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.lineEdit_spotify_client_id = QtWidgets.QLineEdit(parent=self.groupBox_spotify_settings)
        self.lineEdit_spotify_client_id.setObjectName("lineEdit_spotify_client_id")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_spotify_client_id)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_spotify_settings)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.lineEdit_spotify_client_secret = QtWidgets.QLineEdit(parent=self.groupBox_spotify_settings)
        self.lineEdit_spotify_client_secret.setObjectName("lineEdit_spotify_client_secret")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_spotify_client_secret)
        self.checkBox_spotify_optionalGroup_auth_token = QtWidgets.QCheckBox(parent=self.groupBox_spotify_settings)
        self.checkBox_spotify_optionalGroup_auth_token.setChecked(False)
        self.checkBox_spotify_optionalGroup_auth_token.setObjectName("checkBox_spotify_optionalGroup_auth_token")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_spotify_optionalGroup_auth_token)
        self.lineEdit_spotify_auth_token = QtWidgets.QLineEdit(parent=self.groupBox_spotify_settings)
        self.lineEdit_spotify_auth_token.setObjectName("lineEdit_spotify_auth_token")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_spotify_auth_token)
        self.checkBox_spotify_user_auth = QtWidgets.QCheckBox(parent=self.groupBox_spotify_settings)
        self.checkBox_spotify_user_auth.setObjectName("checkBox_spotify_user_auth")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_spotify_user_auth)
        self.checkBox_spotify_headless = QtWidgets.QCheckBox(parent=self.groupBox_spotify_settings)
        self.checkBox_spotify_headless.setObjectName("checkBox_spotify_headless")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_spotify_headless)
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_spotify_settings)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox_spotify_settings)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(21, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_9)
        self.spinBox_spotify_max_retries = QtWidgets.QSpinBox(parent=self.groupBox_spotify_settings)
        self.spinBox_spotify_max_retries.setObjectName("spinBox_spotify_max_retries")
        self.formLayout.setWidget(21, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox_spotify_max_retries)
        self.cache_path_group = QtWidgets.QWidget(parent=self.groupBox_spotify_settings)
        self.cache_path_group.setObjectName("cache_path_group")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.cache_path_group)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_spotify_cache_path = QtWidgets.QLineEdit(parent=self.cache_path_group)
        self.lineEdit_spotify_cache_path.setObjectName("lineEdit_spotify_cache_path")
        self.horizontalLayout.addWidget(self.lineEdit_spotify_cache_path)
        self.toolButton_cache_path_pick = QtWidgets.QToolButton(parent=self.cache_path_group)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/bxs-folder-plus.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton_cache_path_pick.setIcon(icon)
        self.toolButton_cache_path_pick.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_cache_path_pick.setObjectName("toolButton_cache_path_pick")
        self.horizontalLayout.addWidget(self.toolButton_cache_path_pick)
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cache_path_group)
        self.checkBox_spotify_no_cache = QtWidgets.QCheckBox(parent=self.groupBox_spotify_settings)
        self.checkBox_spotify_no_cache.setObjectName("checkBox_spotify_no_cache")
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_spotify_no_cache)
        self.checkBox_spotify_use_cache_file = QtWidgets.QCheckBox(parent=self.groupBox_spotify_settings)
        self.checkBox_spotify_use_cache_file.setObjectName("checkBox_spotify_use_cache_file")
        self.formLayout.setWidget(17, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_spotify_use_cache_file)
        self.verticalLayout.addWidget(self.groupBox_spotify_settings)
        self.groupBox_downloader_settings = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents)
        self.groupBox_downloader_settings.setObjectName("groupBox_downloader_settings")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_downloader_settings)
        self.formLayout_2.setObjectName("formLayout_2")
        self.checkBox_downloader_optionalGroup_bitrate = QtWidgets.QCheckBox(parent=self.groupBox_downloader_settings)
        self.checkBox_downloader_optionalGroup_bitrate.setObjectName("checkBox_downloader_optionalGroup_bitrate")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_downloader_optionalGroup_bitrate)
        self.comboBox_downloader_bitrate = QtWidgets.QComboBox(parent=self.groupBox_downloader_settings)
        self.comboBox_downloader_bitrate.setObjectName("comboBox_downloader_bitrate")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBox_downloader_bitrate)
        self.label_11 = QtWidgets.QLabel(parent=self.groupBox_downloader_settings)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_11)
        self.comboBox_downloader_format = QtWidgets.QComboBox(parent=self.groupBox_downloader_settings)
        self.comboBox_downloader_format.setObjectName("comboBox_downloader_format")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBox_downloader_format)
        self.label_20 = QtWidgets.QLabel(parent=self.groupBox_downloader_settings)
        self.label_20.setObjectName("label_20")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_20)
        self.spinBox_downloader_threads = QtWidgets.QSpinBox(parent=self.groupBox_downloader_settings)
        self.spinBox_downloader_threads.setMaximum(61)
        self.spinBox_downloader_threads.setProperty("value", 4)
        self.spinBox_downloader_threads.setObjectName("spinBox_downloader_threads")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox_downloader_threads)
        self.checkBox_downloader_optionalGroup_cookie_file = QtWidgets.QCheckBox(parent=self.groupBox_downloader_settings)
        self.checkBox_downloader_optionalGroup_cookie_file.setObjectName("checkBox_downloader_optionalGroup_cookie_file")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_downloader_optionalGroup_cookie_file)
        self.checkBox_downloader_sponsorblock = QtWidgets.QCheckBox(parent=self.groupBox_downloader_settings)
        self.checkBox_downloader_sponsorblock.setObjectName("checkBox_downloader_sponsorblock")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_downloader_sponsorblock)
        self.checkBox_downloader_print_errors = QtWidgets.QCheckBox(parent=self.groupBox_downloader_settings)
        self.checkBox_downloader_print_errors.setObjectName("checkBox_downloader_print_errors")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_downloader_print_errors)
        self.checkBox_downloader_playlist_numbering = QtWidgets.QCheckBox(parent=self.groupBox_downloader_settings)
        self.checkBox_downloader_playlist_numbering.setObjectName("checkBox_downloader_playlist_numbering")
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_downloader_playlist_numbering)
        self.checkBox_downloader_scan_for_songs = QtWidgets.QCheckBox(parent=self.groupBox_downloader_settings)
        self.checkBox_downloader_scan_for_songs.setObjectName("checkBox_downloader_scan_for_songs")
        self.formLayout_2.setWidget(13, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_downloader_scan_for_songs)
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_downloader_settings)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(14, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7)
        self.comboBox_downloader_overwrite = QtWidgets.QComboBox(parent=self.groupBox_downloader_settings)
        self.comboBox_downloader_overwrite.setObjectName("comboBox_downloader_overwrite")
        self.formLayout_2.setWidget(14, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBox_downloader_overwrite)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_downloader_settings)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(15, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.lineEdit_downloader_output = QtWidgets.QLineEdit(parent=self.groupBox_downloader_settings)
        self.lineEdit_downloader_output.setObjectName("lineEdit_downloader_output")
        self.formLayout_2.setWidget(15, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_downloader_output)
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_downloader_settings)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(17, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.checkBox_downloader_optionalGroup_ffmpeg_args = QtWidgets.QCheckBox(parent=self.groupBox_downloader_settings)
        self.checkBox_downloader_optionalGroup_ffmpeg_args.setChecked(False)
        self.checkBox_downloader_optionalGroup_ffmpeg_args.setObjectName("checkBox_downloader_optionalGroup_ffmpeg_args")
        self.formLayout_2.setWidget(18, QtWidgets.QFormLayout.ItemRole.LabelRole, self.checkBox_downloader_optionalGroup_ffmpeg_args)
        self.lineEdit_downloader_ffmpeg_args = QtWidgets.QLineEdit(parent=self.groupBox_downloader_settings)
        self.lineEdit_downloader_ffmpeg_args.setObjectName("lineEdit_downloader_ffmpeg_args")
        self.formLayout_2.setWidget(18, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_downloader_ffmpeg_args)
        self.cookie_file_group = QtWidgets.QWidget(parent=self.groupBox_downloader_settings)
        self.cookie_file_group.setObjectName("cookie_file_group")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.cookie_file_group)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_downloader_cookie_file = QtWidgets.QLineEdit(parent=self.cookie_file_group)
        self.lineEdit_downloader_cookie_file.setObjectName("lineEdit_downloader_cookie_file")
        self.horizontalLayout_2.addWidget(self.lineEdit_downloader_cookie_file)
        self.toolButton_cookie_file_pick = QtWidgets.QToolButton(parent=self.cookie_file_group)
        self.toolButton_cookie_file_pick.setIcon(icon)
        self.toolButton_cookie_file_pick.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_cookie_file_pick.setObjectName("toolButton_cookie_file_pick")
        self.horizontalLayout_2.addWidget(self.toolButton_cookie_file_pick)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cookie_file_group)
        self.ffmpeg_group = QtWidgets.QWidget(parent=self.groupBox_downloader_settings)
        self.ffmpeg_group.setObjectName("ffmpeg_group")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.ffmpeg_group)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit_downloader_ffmpeg = QtWidgets.QLineEdit(parent=self.ffmpeg_group)
        self.lineEdit_downloader_ffmpeg.setObjectName("lineEdit_downloader_ffmpeg")
        self.horizontalLayout_3.addWidget(self.lineEdit_downloader_ffmpeg)
        self.toolButton_ffmpeg_pick = QtWidgets.QToolButton(parent=self.ffmpeg_group)
        self.toolButton_ffmpeg_pick.setIcon(icon)
        self.toolButton_ffmpeg_pick.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_ffmpeg_pick.setObjectName("toolButton_ffmpeg_pick")
        self.horizontalLayout_3.addWidget(self.toolButton_ffmpeg_pick)
        self.formLayout_2.setWidget(17, QtWidgets.QFormLayout.ItemRole.FieldRole, self.ffmpeg_group)
        self.verticalLayout.addWidget(self.groupBox_downloader_settings)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Settings)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Apply|QtWidgets.QDialogButtonBox.StandardButton.Discard)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Settings)
        self.checkBox_spotify_optionalGroup_auth_token.toggled['bool'].connect(self.lineEdit_spotify_auth_token.setVisible) # type: ignore
        self.buttonBox.accepted.connect(Settings.accept) # type: ignore
        self.buttonBox.rejected.connect(Settings.reject) # type: ignore
        self.checkBox_downloader_optionalGroup_ffmpeg_args.toggled['bool'].connect(self.lineEdit_downloader_ffmpeg_args.setVisible) # type: ignore
        self.checkBox_downloader_optionalGroup_bitrate.toggled['bool'].connect(self.comboBox_downloader_bitrate.setVisible) # type: ignore
        self.checkBox_downloader_optionalGroup_cookie_file.toggled['bool'].connect(self.cookie_file_group.setVisible) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.groupBox_spotify_settings.setTitle(_translate("Settings", "Spotify Settings"))
        self.label.setText(_translate("Settings", "Client ID"))
        self.label_2.setText(_translate("Settings", "Clinet Secret"))
        self.checkBox_spotify_optionalGroup_auth_token.setText(_translate("Settings", "Use Auth Token"))
        self.checkBox_spotify_user_auth.setText(_translate("Settings", "User Auth"))
        self.checkBox_spotify_headless.setText(_translate("Settings", "Headless"))
        self.label_6.setText(_translate("Settings", "Cache Path"))
        self.label_9.setText(_translate("Settings", "Max Retries"))
        self.toolButton_cache_path_pick.setText(_translate("Settings", "..."))
        self.checkBox_spotify_no_cache.setText(_translate("Settings", "No Cache"))
        self.checkBox_spotify_use_cache_file.setText(_translate("Settings", "Use Cache File"))
        self.groupBox_downloader_settings.setTitle(_translate("Settings", "Downloader Settings"))
        self.checkBox_downloader_optionalGroup_bitrate.setText(_translate("Settings", "Custom Bitrate"))
        self.label_11.setText(_translate("Settings", "Format"))
        self.label_20.setText(_translate("Settings", "Threads"))
        self.checkBox_downloader_optionalGroup_cookie_file.setText(_translate("Settings", "Set Cookie File"))
        self.checkBox_downloader_sponsorblock.setText(_translate("Settings", "Sponsorblock"))
        self.checkBox_downloader_print_errors.setText(_translate("Settings", "Print Errors"))
        self.checkBox_downloader_playlist_numbering.setText(_translate("Settings", "Playlist Numbering"))
        self.checkBox_downloader_scan_for_songs.setText(_translate("Settings", "Scan for songs"))
        self.label_7.setText(_translate("Settings", "Overwrite"))
        self.label_3.setText(_translate("Settings", "Output"))
        self.label_8.setText(_translate("Settings", "FFmpeg EXE"))
        self.checkBox_downloader_optionalGroup_ffmpeg_args.setText(_translate("Settings", "Set FFmpeg Args"))
        self.toolButton_cookie_file_pick.setText(_translate("Settings", "..."))
        self.toolButton_ffmpeg_pick.setText(_translate("Settings", "..."))
