# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_character_map.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CharacterMapDialog(object):
    def setupUi(self, CharacterMapDialog):
        CharacterMapDialog.setObjectName("CharacterMapDialog")
        CharacterMapDialog.resize(540, 520)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CharacterMapDialog.sizePolicy().hasHeightForWidth())
        CharacterMapDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(CharacterMapDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableCharMap = QtWidgets.QTableWidget(CharacterMapDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableCharMap.sizePolicy().hasHeightForWidth())
        self.tableCharMap.setSizePolicy(sizePolicy)
        self.tableCharMap.setMinimumSize(QtCore.QSize(0, 0))
        self.tableCharMap.setIconSize(QtCore.QSize(0, 0))
        self.tableCharMap.setRowCount(12)
        self.tableCharMap.setColumnCount(12)
        self.tableCharMap.setObjectName("tableCharMap")
        self.tableCharMap.horizontalHeader().setVisible(False)
        self.tableCharMap.horizontalHeader().setDefaultSectionSize(40)
        self.tableCharMap.horizontalHeader().setMinimumSectionSize(40)
        self.tableCharMap.verticalHeader().setVisible(False)
        self.tableCharMap.verticalHeader().setDefaultSectionSize(40)
        self.tableCharMap.verticalHeader().setHighlightSections(True)
        self.tableCharMap.verticalHeader().setMinimumSectionSize(40)
        self.tableCharMap.verticalHeader().setSortIndicatorShown(False)
        self.tableCharMap.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableCharMap)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnInsertChar = QtWidgets.QPushButton(CharacterMapDialog)
        self.btnInsertChar.setObjectName("btnInsertChar")
        self.horizontalLayout.addWidget(self.btnInsertChar)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CharacterMapDialog)
        QtCore.QMetaObject.connectSlotsByName(CharacterMapDialog)

    def retranslateUi(self, CharacterMapDialog):
        _translate = QtCore.QCoreApplication.translate
        CharacterMapDialog.setWindowTitle(_translate("CharacterMapDialog", "Special Characters Font Map"))
        self.btnInsertChar.setText(_translate("CharacterMapDialog", "Insert Special Character"))

