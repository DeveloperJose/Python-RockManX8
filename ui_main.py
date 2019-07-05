import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog

from ui_editor_window import EditorWindow

LANGUAGES = ['SPA - [Spanish]', 'ENG - [English]', 'CHI - [Chinese]', 'FRE - [French]', 'GER - [German]', 'ITA - [Italian]', 'JPN - [Japanese]', 'KOR - [Korean]', 'USA - [PS2 English]']

app = QtWidgets.QApplication([])

# == Settings
# pyuic5 ui_design_editor.ui -o ui_design_editor.py
prompt, language_selected = QInputDialog.getItem(None, 'Language Select', 'Please select the language to edit', LANGUAGES, 0, False)
if language_selected:
    language = prompt.split('-')[0].strip()

    installation_path = ''
    while not os.path.exists(os.path.join(installation_path, 'mes', language)):
        installation_path = str(QFileDialog.getExistingDirectory(None, caption='Please select your X8 installation folder (must contain a /mes/ directory)', directory=''))

    application = EditorWindow(installation_path, language)
    application.show()
    # sys.exit(app.exec())
