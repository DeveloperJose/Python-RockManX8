import subprocess
import pickle
from pathlib import Path

from core.wpg import Font
from app import config

# Manager Settings
default_font_path = Path('resources//default_font.wpg')
arctool_path = Path('resources//ARCtool.exe')
mugshots_path = Path('resources//mugshots.pkl')

if not arctool_path.exists():
    raise Exception(f'Could not find resource: {arctool_path}')

if not default_font_path.exists():
    raise Exception(f'Could not find resource: {default_font_path}')

if not mugshots_path.exists():
    raise Exception(f'Could not find resource: {mugshots_path}')

class __Resources__:
    @property
    def font_path(self) -> Path:
        if config.is_valid_collection:
            return default_font_path
        return config.install_path / 'opk' / 'title' / config.language.lower() / 'wpg' / 'font_ID_FONT_000.wpg'

    @property
    def font(self) -> Font:
        return Font(self.font_path)

    @property
    def mugshots(self):
        return pickle.load(open(mugshots_path, 'rb'))


resources = __Resources__()


def arctool_extract(fpath):
    subprocess.call([str(arctool_path), '-x', '-pc', '-silent', str(fpath)], creationflags=subprocess.CREATE_NO_WINDOW)


def arctool_compress(fpath):
    subprocess.call([str(arctool_path), '-c', '-pc', '-silent', str(fpath)], creationflags=subprocess.CREATE_NO_WINDOW)
