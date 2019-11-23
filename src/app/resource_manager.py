import subprocess
import numpy as np
from pathlib import Path
from typing import List

from core.wpg import Font
from app import config

# Manager Settings
default_font_path = Path('resources//font.wpg')
arctool_path = Path('resources//ARCtool.exe')
mugshots_path = Path('resources//mugshots.npz')

if not arctool_path.exists() or not default_font_path.exists() or not mugshots_path.exists():
    raise Exception('Could not load resources from resources folder')


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
    def mugshots(self) -> List[np.ndarray]:
        return np.load(str(mugshots_path), allow_pickle=True)['mugshots']


resources = __Resources__()


def arctool_extract(fpath):
    subprocess.call([str(arctool_path), '-x', '-pc', '-silent', str(fpath)], creationflags=subprocess.CREATE_NO_WINDOW)


def arctool_compress(fpath):
    subprocess.call([str(arctool_path), '-c', '-pc', '-silent', str(fpath)], creationflags=subprocess.CREATE_NO_WINDOW)
