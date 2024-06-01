# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'text_editor.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(660, 424)
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
        self.groupFile = QtWidgets.QGroupBox(self.centralwidget)
        self.groupFile.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupFile.setFont(font)
        self.groupFile.setStyleSheet(
            "QGroupBox { \n"
            "    background: rgb(255, 170, 0);\n"
            "    color: rgb(255, 255, 255)\n"
            "}"
        )
        self.groupFile.setObjectName("groupFile")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupFile)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboFiles = QtWidgets.QComboBox(self.groupFile)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboFiles.sizePolicy().hasHeightForWidth())
        self.comboFiles.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboFiles.setFont(font)
        self.comboFiles.setObjectName("comboFiles")
        self.horizontalLayout.addWidget(self.comboFiles)
        self.btnOpenCloseFile = QtWidgets.QPushButton(self.groupFile)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnOpenCloseFile.sizePolicy().hasHeightForWidth()
        )
        self.btnOpenCloseFile.setSizePolicy(sizePolicy)
        self.btnOpenCloseFile.setObjectName("btnOpenCloseFile")
        self.horizontalLayout.addWidget(self.btnOpenCloseFile)
        self.verticalLayout_4.addWidget(self.groupFile)
        self.groupText = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupText.sizePolicy().hasHeightForWidth())
        self.groupText.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupText.setFont(font)
        self.groupText.setStyleSheet("")
        self.groupText.setObjectName("groupText")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupText)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint
        )
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.groupText)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.spinCurrentText = QtWidgets.QSpinBox(self.groupText)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.spinCurrentText.sizePolicy().hasHeightForWidth()
        )
        self.spinCurrentText.setSizePolicy(sizePolicy)
        self.spinCurrentText.setMinimumSize(QtCore.QSize(0, 0))
        self.spinCurrentText.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.spinCurrentText.setFont(font)
        self.spinCurrentText.setObjectName("spinCurrentText")
        self.horizontalLayout_2.addWidget(self.spinCurrentText)
        self.label_2 = QtWidgets.QLabel(self.groupText)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lblTotalTexts = QtWidgets.QLabel(self.groupText)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lblTotalTexts.sizePolicy().hasHeightForWidth()
        )
        self.lblTotalTexts.setSizePolicy(sizePolicy)
        self.lblTotalTexts.setMinimumSize(QtCore.QSize(0, 0))
        self.lblTotalTexts.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblTotalTexts.setFont(font)
        self.lblTotalTexts.setMouseTracking(True)
        self.lblTotalTexts.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lblTotalTexts.setLineWidth(1)
        self.lblTotalTexts.setTextFormat(QtCore.Qt.RichText)
        self.lblTotalTexts.setScaledContents(False)
        self.lblTotalTexts.setObjectName("lblTotalTexts")
        self.horizontalLayout_2.addWidget(self.lblTotalTexts)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textEditor = QtWidgets.QTextEdit(self.groupText)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditor.sizePolicy().hasHeightForWidth())
        self.textEditor.setSizePolicy(sizePolicy)
        self.textEditor.setMaximumSize(QtCore.QSize(9999999, 100))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.textEditor.setFont(font)
        self.textEditor.setObjectName("textEditor")
        self.verticalLayout.addWidget(self.textEditor)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.btnOpenCharMap = QtWidgets.QPushButton(self.groupText)
        self.btnOpenCharMap.setObjectName("btnOpenCharMap")
        self.horizontalLayout_7.addWidget(self.btnOpenCharMap)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_7.addItem(spacerItem2)
        self.btnSave = QtWidgets.QPushButton(self.groupText)
        self.btnSave.setEnabled(False)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_7.addWidget(self.btnSave)
        self.btnRevert = QtWidgets.QPushButton(self.groupText)
        self.btnRevert.setObjectName("btnRevert")
        self.horizontalLayout_7.addWidget(self.btnRevert)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4.addWidget(self.groupText)
        self.groupExtraData = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupExtraData.sizePolicy().hasHeightForWidth()
        )
        self.groupExtraData.setSizePolicy(sizePolicy)
        self.groupExtraData.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupExtraData.setFont(font)
        self.groupExtraData.setAutoFillBackground(False)
        self.groupExtraData.setStyleSheet(
            "QGroupBox, QLabel, QCheckBox { \n"
            "    background-color: rgb(0, 170, 255);\n"
            "    color: white;\n"
            '    font: 12pt "Calibri";\n'
            "}\n"
            "\n"
            "QLineEdit, QSpinBox {\n"
            '    font: 12pt "Calibri";\n'
            "}\n"
            "\n"
            "QGroupBox {\n"
            '    font: 15pt "Calibri";\n'
            "}"
        )
        self.groupExtraData.setFlat(False)
        self.groupExtraData.setCheckable(False)
        self.groupExtraData.setObjectName("groupExtraData")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupExtraData)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_4.addItem(spacerItem3)
        self.label_5 = QtWidgets.QLabel(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.label_5.setFont(font)
        self.label_5.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.textFilename = QtWidgets.QLineEdit(self.groupExtraData)
        self.textFilename.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textFilename.sizePolicy().hasHeightForWidth())
        self.textFilename.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.textFilename.setFont(font)
        self.textFilename.setReadOnly(True)
        self.textFilename.setClearButtonEnabled(False)
        self.textFilename.setObjectName("textFilename")
        self.horizontalLayout_4.addWidget(self.textFilename)
        self.label_10 = QtWidgets.QLabel(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.comboCharacter = QtWidgets.QComboBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboCharacter.sizePolicy().hasHeightForWidth()
        )
        self.comboCharacter.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.comboCharacter.setFont(font)
        self.comboCharacter.setObjectName("comboCharacter")
        self.horizontalLayout_4.addWidget(self.comboCharacter)
        self.label_11 = QtWidgets.QLabel(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.spinMugshot = QtWidgets.QSpinBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinMugshot.sizePolicy().hasHeightForWidth())
        self.spinMugshot.setSizePolicy(sizePolicy)
        self.spinMugshot.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.spinMugshot.setFont(font)
        self.spinMugshot.setObjectName("spinMugshot")
        self.horizontalLayout_3.addWidget(self.spinMugshot)
        self.textMugshotDesc = QtWidgets.QLineEdit(self.groupExtraData)
        self.textMugshotDesc.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textMugshotDesc.sizePolicy().hasHeightForWidth()
        )
        self.textMugshotDesc.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.textMugshotDesc.setFont(font)
        self.textMugshotDesc.setObjectName("textMugshotDesc")
        self.horizontalLayout_3.addWidget(self.textMugshotDesc)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_5.addItem(spacerItem5)
        self.label_12 = QtWidgets.QLabel(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_5.addWidget(self.label_12)
        self.comboMugshotPos = QtWidgets.QComboBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboMugshotPos.sizePolicy().hasHeightForWidth()
        )
        self.comboMugshotPos.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.comboMugshotPos.setFont(font)
        self.comboMugshotPos.setObjectName("comboMugshotPos")
        self.horizontalLayout_5.addWidget(self.comboMugshotPos)
        self.label_13 = QtWidgets.QLabel(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_5.addWidget(self.label_13)
        self.comboTextPos = QtWidgets.QComboBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboTextPos.sizePolicy().hasHeightForWidth())
        self.comboTextPos.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.comboTextPos.setFont(font)
        self.comboTextPos.setObjectName("comboTextPos")
        self.horizontalLayout_5.addWidget(self.comboTextPos)
        self.label_6 = QtWidgets.QLabel(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.comboVoice = QtWidgets.QComboBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboVoice.sizePolicy().hasHeightForWidth())
        self.comboVoice.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.comboVoice.setFont(font)
        self.comboVoice.setObjectName("comboVoice")
        self.horizontalLayout_5.addWidget(self.comboVoice)
        self.label_7 = QtWidgets.QLabel(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.comboBGM = QtWidgets.QComboBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBGM.sizePolicy().hasHeightForWidth())
        self.comboBGM.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.comboBGM.setFont(font)
        self.comboBGM.setObjectName("comboBGM")
        self.horizontalLayout_5.addWidget(self.comboBGM)
        self.label_9 = QtWidgets.QLabel(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.spinCameraAngle = QtWidgets.QSpinBox(self.groupExtraData)
        self.spinCameraAngle.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.spinCameraAngle.sizePolicy().hasHeightForWidth()
        )
        self.spinCameraAngle.setSizePolicy(sizePolicy)
        self.spinCameraAngle.setMinimumSize(QtCore.QSize(0, 0))
        self.spinCameraAngle.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.spinCameraAngle.setFont(font)
        self.spinCameraAngle.setObjectName("spinCameraAngle")
        self.horizontalLayout_5.addWidget(self.spinCameraAngle)
        spacerItem6 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_5.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem7 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_6.addItem(spacerItem7)
        self.checkStopBGM = QtWidgets.QCheckBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkStopBGM.sizePolicy().hasHeightForWidth())
        self.checkStopBGM.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.checkStopBGM.setFont(font)
        self.checkStopBGM.setObjectName("checkStopBGM")
        self.horizontalLayout_6.addWidget(self.checkStopBGM)
        self.checkArrow = QtWidgets.QCheckBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkArrow.sizePolicy().hasHeightForWidth())
        self.checkArrow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.checkArrow.setFont(font)
        self.checkArrow.setObjectName("checkArrow")
        self.horizontalLayout_6.addWidget(self.checkArrow)
        self.checkTyping = QtWidgets.QCheckBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkTyping.sizePolicy().hasHeightForWidth())
        self.checkTyping.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.checkTyping.setFont(font)
        self.checkTyping.setObjectName("checkTyping")
        self.horizontalLayout_6.addWidget(self.checkTyping)
        self.checkCloseTop = QtWidgets.QCheckBox(self.groupExtraData)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.checkCloseTop.sizePolicy().hasHeightForWidth()
        )
        self.checkCloseTop.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.checkCloseTop.setFont(font)
        self.checkCloseTop.setObjectName("checkCloseTop")
        self.horizontalLayout_6.addWidget(self.checkCloseTop)
        spacerItem8 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_6.addItem(spacerItem8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_4.addWidget(self.groupExtraData)
        self.groupPreview = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupPreview.sizePolicy().hasHeightForWidth())
        self.groupPreview.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupPreview.setFont(font)
        self.groupPreview.setStyleSheet("background: black;\n" "color: white;")
        self.groupPreview.setObjectName("groupPreview")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupPreview)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.graphicsMugshot = QtWidgets.QLabel(self.groupPreview)
        self.graphicsMugshot.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsMugshot.setMaximumSize(QtCore.QSize(128, 128))
        self.graphicsMugshot.setObjectName("graphicsMugshot")
        self.horizontalLayout_8.addWidget(self.graphicsMugshot)
        self.graphicsPreview = QtWidgets.QLabel(self.groupPreview)
        self.graphicsPreview.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsPreview.setMaximumSize(QtCore.QSize(1000, 1000))
        self.graphicsPreview.setObjectName("graphicsPreview")
        self.horizontalLayout_8.addWidget(self.graphicsPreview)
        self.verticalLayout_4.addWidget(self.groupPreview)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Title Will Be Set In Code"))
        self.groupFile.setTitle(_translate("MainWindow", "File"))
        self.btnOpenCloseFile.setText(_translate("MainWindow", "Open File"))
        self.groupText.setTitle(_translate("MainWindow", "Text Editor"))
        self.label.setText(_translate("MainWindow", "Current Text:"))
        self.label_2.setText(_translate("MainWindow", "/"))
        self.lblTotalTexts.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" color:#aa0000;">47</span></p></body></html>',
            )
        )
        self.textEditor.setDocumentTitle(_translate("MainWindow", "Title"))
        self.textEditor.setHtml(
            _translate(
                "MainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><title>Title</title><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Consolas'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Example Text</p></body></html>',
            )
        )
        self.btnOpenCharMap.setText(_translate("MainWindow", "Open Character Map"))
        self.btnSave.setText(_translate("MainWindow", "Save Changes"))
        self.btnRevert.setText(_translate("MainWindow", "Revert"))
        self.groupExtraData.setTitle(_translate("MainWindow", "Extra Data Editor"))
        self.label_5.setText(_translate("MainWindow", "Filename"))
        self.label_10.setText(_translate("MainWindow", "Character"))
        self.label_11.setText(_translate("MainWindow", "Mugshot"))
        self.label_12.setText(_translate("MainWindow", "Mugshot Position"))
        self.label_13.setText(_translate("MainWindow", "Text Position"))
        self.label_6.setText(_translate("MainWindow", "Voice"))
        self.label_7.setText(_translate("MainWindow", "BGM"))
        self.label_9.setText(_translate("MainWindow", "Camera Angle"))
        self.spinCameraAngle.setSpecialValueText(_translate("MainWindow", "N/A"))
        self.checkStopBGM.setText(_translate("MainWindow", "Stop all BGM"))
        self.checkArrow.setText(_translate("MainWindow", "Show an Arrow"))
        self.checkTyping.setText(_translate("MainWindow", "Type One Letter At A Time"))
        self.checkCloseTop.setText(_translate("MainWindow", "Close Top Dialogue"))
        self.groupPreview.setTitle(_translate("MainWindow", "Preview"))
        self.graphicsMugshot.setText(_translate("MainWindow", "Mugshot Will Go Here"))
        self.graphicsPreview.setText(_translate("MainWindow", "Text Will Go Here"))
