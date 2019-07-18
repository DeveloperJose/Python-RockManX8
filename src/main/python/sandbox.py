from pathlib import Path

import PyQt5.QtCore as QtCore
import qimage2ndarray
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QDialog

from ui_character_map import Ui_CharacterMapDialog
from x8_utils import Font


class CharacterMapDialog(QDialog):
    def __init__(self):
        super(QDialog, self).__init__(None)
        self.ui = Ui_CharacterMapDialog()
        self.ui.setupUi(self)

        font = Font(Path(r'C:\Users\xeroj\Desktop\Local_Programming\RockManX8_Tools\game\opk\title\spa\wpg\font_ID_FONT_000.wpg'))
        chars = font.characters

        col_count = 12
        row_count = len(chars) // col_count
        chars = chars.reshape(row_count, col_count, 20, 20)

        self.ui.tableCharMap.setRowCount(row_count)
        self.ui.tableCharMap.setColumnCount(col_count)
        self.ui.tableCharMap.setIconSize(QtCore.QSize(40, 40))

        for row_idx, col_arr in enumerate(chars):
            for col_idx, im_char in enumerate(col_arr):
                idx = (row_idx * col_count) + col_idx

                q_im = qimage2ndarray.array2qimage(im_char)
                pixmap = QPixmap(q_im).scaled(40, 40)
                icon = QIcon(pixmap)
                item = QTableWidgetItem(icon, str(idx))
                self.ui.tableCharMap.setItem(row_idx, col_idx, item)

    def set_btn_callback(self, callback):
        self.ui.btnInsertChar.clicked.connect(callback)

    def get_selected_char_byte(self):
        return self.ui.tableCharMap.selectedItems()[0].text()

app = QApplication([])
# window = QMainWindow()
# window.show()

dialog = CharacterMapDialog()
dialog.set_btn_callback(lambda: print(dialog.get_selected_char_byte()))
dialog.exec_()

# app.exec_()
