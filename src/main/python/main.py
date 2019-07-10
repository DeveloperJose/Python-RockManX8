import os
import sys

from PyQt5.QtWidgets import QFileDialog, QInputDialog, QApplication

from fbs_utils import AppContext
from ui_editor_window import EditorWindow

LANGUAGES = ['SPA - [Spanish]', 'ENG - [English]', 'CHI - [Chinese]', 'FRE - [French]', 'GER - [German]', 'ITA - [Italian]', 'JPN - [Japanese]', 'KOR - [Korean]', 'USA - [PS2 English]']


def pre_initialization():
    prompt, language_selected = QInputDialog.getItem(None, 'Language Select', 'Please select the language to edit'.ljust(50), LANGUAGES, 0, False)
    if language_selected:
        lang_folder = prompt.split('-')[0].strip()

        x8_installation_path = 'C:/Users/xeroj/Desktop/Local_Programming/RockManX8_Tools/Game'
        while not os.path.exists(os.path.join(x8_installation_path, 'mes', lang_folder)):
            x8_installation_path = QFileDialog.getExistingDirectory(None, caption='Please select your X8 installation folder (must contain a /mes/ directory)', directory='')

            if x8_installation_path == '':
                return False, False
    else:
        return False, False

    return x8_installation_path, lang_folder


if __name__ == '__main__':
    app = QApplication([])
    appctxt = AppContext()
    installation_path, language = pre_initialization()
    window_title = 'MegaManX8 Text Editor by RainfallPianist [{}]'.format(appctxt.build_settings['version'])

    if not installation_path:
        sys.exit(0)

    application = EditorWindow(installation_path, language)
    application.setWindowTitle(window_title)
    appctxt.ui = application.ui

    application.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
