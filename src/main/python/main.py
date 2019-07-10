import os
import sys
import subprocess
import configparser

from PyQt5.QtWidgets import QFileDialog, QInputDialog, QApplication

from fbs_utils import AppContext
from ui_editor_window import EditorWindow

LANGUAGES = ['SPA - [Spanish]', 'USA - [English (USA)]', 'ENG - [English (Europe)]', 'CHI - [Chinese]', 'FRE - [French]', 'GER - [German]', 'ITA - [Italian]', 'JPN - [Japanese]', 'KOR - [Korean]']
SETTINGS_PATH = 'settings.ini'


def prompt_language():
    prompt, language_selected = QInputDialog.getItem(None, 'Language Select', 'Please select the language to edit'.ljust(50), LANGUAGES, 0, False)

    if language_selected:
        lang_folder = prompt.split('-')[0].strip()
        return lang_folder
    return False


def prompt_installation():
    install_path = ''

    while True:
        install_path = QFileDialog.getExistingDirectory(None, caption='Please select your X8 or Legacy Collection installation folder', directory='')
        if install_path == '':
            return False

        valid_x8 = os.path.exists(os.path.join(install_path, 'mes'))
        valid_collection = os.path.exists(os.path.join(install_path, 'nativeDX10', 'X8', 'romPC', 'data', 'mes'))

        if valid_x8 or valid_collection:
            return install_path


def load_config():
    cfg = configparser.ConfigParser()
    if os.path.exists(SETTINGS_PATH):
        cfg.read(SETTINGS_PATH)
    else:
        install_path = prompt_installation()
        lang_folder = prompt_language()
        is_valid_collection = os.path.exists(os.path.join(install_path, 'nativeDX10', 'X8', 'romPC', 'data', 'mes'))

        if not install_path or not lang_folder:
            return False

        cfg.add_section('editor')
        cfg.set('editor', 'language', lang_folder)
        cfg.set('editor', 'installation_path', install_path)
        cfg.set('editor', 'is_legacy_collection', str(is_valid_collection))

        with open(SETTINGS_PATH, 'w') as cfgfile:
            cfg.write(cfgfile)

    return cfg


if __name__ == '__main__':
    app = QApplication([])
    appctxt = AppContext()
    window_title = 'MegaManX8 Text Editor by RainfallPianist [{}]'.format(appctxt.build_settings['version'])

    config = load_config()
    if not config:
        sys.exit(0)

    application = EditorWindow(appctxt, config)
    application.setWindowTitle(window_title)
    appctxt.editor = application

    application.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
