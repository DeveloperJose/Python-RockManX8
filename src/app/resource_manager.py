import subprocess
import pickle
import sys
import os
from pathlib import Path

from core.wpg import Font
from app import config


def __resource_path__(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("..")

    return Path(os.path.join(base_path, relative_path))


# Manager Settings
__default_font_path__ = __resource_path__('resources//default_font.wpg')
__arctool_path__ = __resource_path__('resources//ARCtool.exe')
__mugshots_path__ = __resource_path__('resources//mugshots.pkl')
__icon_path__ = __resource_path__('resources//icon.png')

if not __arctool_path__.exists():
    raise Exception(f'Could not find resource: {__arctool_path__}')

if not __default_font_path__.exists():
    raise Exception(f'Could not find resource: {__default_font_path__}')

if not __mugshots_path__.exists():
    raise Exception(f'Could not find resource: {__mugshots_path__}')

if not __icon_path__.exists():
    raise Exception(f'Could not find resource: {__icon_path__}')


class __Resources__:
    @property
    def font_path(self) -> Path:
        if config.is_valid_collection:
            return __default_font_path__
        return config.install_path / 'opk' / 'title' / config.language.lower() / 'wpg' / 'font_ID_FONT_000.wpg'

    @property
    def font(self) -> Font:
        return Font(self.font_path)

    @property
    def mugshots(self):
        return pickle.load(open(__mugshots_path__, 'rb'))

    @property
    def icon_path(self):
        return str(__icon_path__)


resources = __Resources__()


def arctool_extract(fpath):
    subprocess.call([str(__arctool_path__), '-x', '-pc', '-silent', str(fpath)], creationflags=subprocess.CREATE_NO_WINDOW)


def arctool_compress(fpath):
    subprocess.call([str(__arctool_path__), '-c', '-pc', '-silent', str(fpath)], creationflags=subprocess.CREATE_NO_WINDOW)
