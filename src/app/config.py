from configparser import ConfigParser
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QInputDialog

# Metadata
author = 'RainfallPianist'
version = 'v1.4-beta'

# Application Variables
window_title = 'MegaManX8 Text Editor by {} [{}]'.format(author, version)
languages = ['SPA - [Spanish]', 'USA - [English (USA)]', 'ENG - [English (Europe)]', 'CHI - [Chinese]', 'FRE - [French]', 'GER - [German]', 'ITA - [Italian]', 'JPN - [Japanese]', 'KOR - [Korean]']

# INI File Settings
config_path = Path('config.ini')
install_path: Path = None
is_valid_collection = False
language = ''


def load_config_or_default():
    if config_path.exists():
        cfg = ConfigParser()
        cfg.read(config_path)
        __load_from_parser__(cfg)
    else:
        install_path = __prompt_installation__()
        if not install_path:
            return False

        lang_folder = __prompt_language__()
        if not lang_folder:
            return False

        is_valid_collection = (install_path / 'nativeDX10' / 'X8' / 'romPC' / 'data' / 'mes').exists()
        __create_default_and_load__(lang_folder, install_path, is_valid_collection)

    return True


def __load_from_parser__(cfg: ConfigParser):
    global install_path, is_valid_collection, language
    install_path = Path(cfg['editor']['installation_path'])
    is_valid_collection = cfg.getboolean('editor', 'is_legacy_collection')
    language = cfg['editor']['language']


def __create_default_and_load__(lang_folder, install_path, is_valid_collection):
    cfg = ConfigParser()
    cfg.add_section('editor')
    cfg.set('editor', 'language', lang_folder)
    cfg.set('editor', 'installation_path', str(install_path))
    cfg.set('editor', 'is_legacy_collection', str(is_valid_collection))

    with open(config_path, 'w') as cfgfile:
        cfg.write(cfgfile)

    __load_from_parser__(cfg)


def __prompt_language__():
    prompt, language_selected = QInputDialog.getItem(None, 'Language Select', 'Please select the language to edit'.ljust(50), languages, 0, False)

    if language_selected:
        lang_folder = prompt.split('-')[0].strip()
        return lang_folder
    return False


def __prompt_installation__():
    while True:
        install_fname = QFileDialog.getExistingDirectory(None, caption='Please select your X8 or Legacy Collection installation folder', directory='')
        if install_fname == '':
            return False

        install_path = Path(install_fname)
        regular_path = install_path / 'mes'
        collection_path = install_path / 'nativeDX10' / 'X8' / 'romPC' / 'data' / 'mes'
        if regular_path.exists() or collection_path.exists():
            return install_path
