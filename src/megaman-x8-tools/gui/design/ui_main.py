# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200, 100)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(2000, 2000))
        MainWindow.setStyleSheet(
            "QMainWindow {\n"
            "    background: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QLabel, QCheckBox { \n"
            "    background: rgb(255, 255, 255);\n"
            '    font: 12pt "Calibri";\n'
            "}\n"
            "\n"
            "QGroupBox {\n"
            "    background: rgb(255, 255, 255);\n"
            '    font: 15pt "Calibri";\n'
            "}\n"
            "\n"
            "QComboBox {\n"
            "    background: white;\n"
            "    color: black;\n"
            "}\n"
            "\n"
            "QPushButton:enabled {\n"
            "    background: rgb(236, 236, 236);\n"
            "    color: black;\n"
            "}\n"
            "\n"
            "QPushButton:disabled, QLineEdit:disabled, QComboBox:disabled{\n"
            "    background: rgb(191, 191, 191);\n"
            "    color: rgb(85, 85, 85);\n"
            "}"
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.uxBtnTextEditor = QtWidgets.QPushButton(self.centralwidget)
        self.uxBtnTextEditor.setObjectName("uxBtnTextEditor")
        self.verticalLayout_4.addWidget(self.uxBtnTextEditor)
        self.uxBtnTextureEditor = QtWidgets.QPushButton(self.centralwidget)
        self.uxBtnTextureEditor.setObjectName("uxBtnTextureEditor")
        self.verticalLayout_4.addWidget(self.uxBtnTextureEditor)
        self.uxBtnLevelEditor = QtWidgets.QPushButton(self.centralwidget)
        self.uxBtnLevelEditor.setObjectName("uxBtnLevelEditor")
        self.verticalLayout_4.addWidget(self.uxBtnLevelEditor)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Title Will Be Set In Code"))
        self.uxBtnTextEditor.setText(_translate("MainWindow", "Open Text Editor"))
        self.uxBtnTextureEditor.setText(_translate("MainWindow", "Open Texture Editor"))
        self.uxBtnLevelEditor.setText(
            _translate("MainWindow", "Open Level Editor (Enemy Placement Only)")
        )
