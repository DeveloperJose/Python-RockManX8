import qimage2ndarray
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QTableWidgetItem

from gui.design.ui_character_map import Ui_CharacterMapDialog
from app import resource_manager


class CharacterMapDialog(QDialog):
    def __init__(self, btn_callback):
        super(QDialog, self).__init__(None)
        self.ui = Ui_CharacterMapDialog()
        self.ui.setupUi(self)

        chars = resource_manager.resources.font.characters
        col_count = 12
        row_count = len(chars) // col_count
        chars = chars.reshape(row_count, col_count, 20, 20)

        self.ui.tableCharMap.setRowCount(row_count)
        self.ui.tableCharMap.setColumnCount(col_count)
        self.ui.tableCharMap.setIconSize(QtCore.QSize(40, 40))
        self.ui.tableCharMap.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.btnInsertChar.clicked.connect(btn_callback)

        for row_idx, col_arr in enumerate(chars):
            for col_idx, im_char in enumerate(col_arr):
                idx = (row_idx * col_count) + col_idx

                q_im = qimage2ndarray.array2qimage(im_char)
                pixmap = QPixmap(q_im).scaled(40, 40)
                icon = QIcon(pixmap)
                item = QTableWidgetItem(icon, str(idx))
                self.ui.tableCharMap.setItem(row_idx, col_idx, item)

    def get_selected_char_byte(self):
        return self.ui.tableCharMap.selectedItems()[0].text()
