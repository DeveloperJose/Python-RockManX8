from pathlib import Path
from core.io_util import FileStream


class WSMFile:
    path: Path

    def __init__(self, path: Path = None):
        self.path = path
        self.header = []
        self.mpeg1_video = []

        if self.path is not None:
            self.__load_from_file__(path)

    def __load_from_file__(self, path: Path):
        with open(path, "rb") as file:
            reader = FileStream(file)

            self.header = reader.read(0x820)
            self.mpeg1_video = reader.read_remaining_bytes()

    def save(self, spath: Path = None):
        if spath is None:
            spath = self.path

        with open(spath, "wb") as file:
            file.write(self.header)
            file.write(self.mpeg1_video)

    def save_video(self, vpath):
        with open(vpath, "wb") as file:
            file.write(self.mpeg1_video)


p = Path(
    r"C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\movie\caplogo - Copy.wsm"
)
output = Path(
    r"C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\movie\caplogo.mpg"
)
wsm = WSMFile(p)
wsm.save_video(output)
