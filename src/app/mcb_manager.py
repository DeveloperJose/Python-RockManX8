import shutil
from pathlib import Path
from PyQt5.QtWidgets import QProgressDialog

from core.x8_utils import MCBFile
from app import config, resource_manager

# Manager Settings
default_collection_mcb_path = Path('arc')


class __Resources__:
    @property
    def arc_folder_path(self):
        return config.install_path / 'nativeDX10' / 'X8' / 'romPC' / 'data' / 'mes' / config.language

    @property
    def mcb_folder_path(self):
        if config.is_valid_collection:
            return default_collection_mcb_path
        return config.install_path / 'mes' / config.language

    @property
    def glob_filter(self):
        if config.is_valid_collection:
            return '*/X8/data/mes/{}/*.0589CBA3'.format(config.language)
        return '*.mcb'


paths = __Resources__()


def extract_collection_arcs():
    if not config.is_valid_collection or paths.mcb_folder_path.exists():
        return

    paths.mcb_folder_path.mkdir()

    diag = QProgressDialog("Extracting Legacy Collection ARC Files", "Cancel", 0, 110)
    diag.setModal(True)

    for idx, fpath in enumerate(paths.arc_folder_path.glob('*.arc')):
        diag.setValue(idx)
        resource_manager.arctool_extract(fpath)
        # Move from legacy collection folder to a local directory (mcb_path)
        # TODO: Perhaps we should copy the arcs and do this locally?
        folder_path = paths.arc_folder_path / fpath.stem
        shutil.move(str(folder_path), str(paths.mcb_folder_path))


def update_collection_mcb(mcb_name):
    if not config.is_valid_collection:
        return

    fpath = paths.mcb_folder_path / mcb_name
    resource_manager.arctool_compress(fpath)

    # Fix the ARC file so it doesn't crash the legacy collection
    arc_name = mcb_name + '.arc'
    arc_file_path = paths.mcb_folder_path / arc_name
    with open(arc_file_path, 'r+b') as file:
        file.seek(4)
        file.write(0x07.to_bytes(1, byteorder='little'))

    # Overwrite legacy ARC file with our own and then delete our copy
    shutil.copy(str(arc_file_path), str(paths.arc_folder_path))
    arc_file_path.unlink()


def get_mcb_names():
    lst = [str(fpath.stem) for fpath in paths.mcb_folder_path.glob(paths.glob_filter)]
    return sorted(lst, key=__mcb_sorting_key__)


def get_mcb(mcb_name):
    return MCBFile(__get_mcb_file_path__(mcb_name))


def __get_mcb_file_path__(mcb_file_name):
    if config.is_valid_collection:
        path = default_collection_mcb_path / mcb_file_name / 'X8/data/mes' / config.language
        ext = '.0589CBA3'
    else:
        path = config.install_path / 'mes' / config.language
        ext = '.mcb'

    fname = mcb_file_name + ext
    return path / fname


def __mcb_sorting_key__(fname: str):
    key = len(fname)
    priorities = ['TRIAL', '_', 'DM', 'ST', 'VA', 'MOV']
    for idx, st in enumerate(priorities):
        if st in fname:
            key += (idx + 1)

    return key
