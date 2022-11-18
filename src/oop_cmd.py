import io
from pathlib import Path
from typing import List

from PIL import Image

from core.io_util import FileStream
from app.resource_manager import arctool_compress, arctool_extract

class OOPFile:

    def __init__(self, path: Path):
        self.path = path

if __name__ == "__main__":
    arc_path = Path('')
    arctool_path = Path('')

    # Extract arc if needed
    original_path = Path('')
    modified_path = Path('')
    
    sigma_file = OOPFile('')