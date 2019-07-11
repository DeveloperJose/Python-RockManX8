import sys
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QInputDialog

from config_utils import Config
from fbs_utils import AppContext
from ui_editor_window import EditorWindow

settings_path = Path('settings.ini')


def prompt_language():
    languages = ['SPA - [Spanish]', 'USA - [English (USA)]', 'ENG - [English (Europe)]', 'CHI - [Chinese]', 'FRE - [French]', 'GER - [German]', 'ITA - [Italian]', 'JPN - [Japanese]', 'KOR - [Korean]']
    prompt, language_selected = QInputDialog.getItem(None, 'Language Select', 'Please select the language to edit'.ljust(50), languages, 0, False)

    if language_selected:
        lang_folder = prompt.split('-')[0].strip()
        return lang_folder
    return False


def prompt_installation():
    while True:
        install_fname = QFileDialog.getExistingDirectory(None, caption='Please select your X8 or Legacy Collection installation folder', directory='')
        if install_fname == '':
            return False

        install_path = Path(install_fname)
        regular_path = install_path / 'mes'
        collection_path = install_path / 'nativeDX10' / 'X8' / 'romPC' / 'data' / 'mes'

        if regular_path.exists() or collection_path.exists():
            return install_fname


def load_config():
    if settings_path.exists():
        cfg = Config.from_path(settings_path)
    else:
        install_path = prompt_installation()
        lang_folder = prompt_language()
        is_valid_collection = (install_path / 'nativeDX10' / 'X8' / 'romPC' / 'data' / 'mes').exists()

        if not install_path or not lang_folder:
            return False

        cfg = Config.create_default(settings_path, lang_folder, install_path, is_valid_collection)

    return cfg


if __name__ == '__main__':
    config = load_config()
    if not config:
        sys.exit(0)

    appctxt = AppContext()
    appctxt.config = config
    window_title = 'MegaManX8 Text Editor by RainfallPianist [{}]'.format(appctxt.build_settings['version'])

    application = EditorWindow(appctxt)
    application.setWindowTitle(window_title)
    application.show()

    appctxt.__editor__ = application
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
