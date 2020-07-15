# Mega Man X8 WPG plugin by Zheneq (https://github.com/Zheneq/Noesis-Plugins)
# Modified by RainfallPianist
#   * Added support for 1BPP TGA
# Made for Noesis 4.428

import noesis
import rapi
from inc_noesis import *


# registerNoesisTypes is called by Noesis to allow the script to register formats.
# Do not implement this function in script files unless you want them to be dedicated format modules!
def registerNoesisTypes():
    handle = noesis.register("Mega Man X8 Texture Archive", ".wpg")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    # noesis.setHandlerWriteRGBA(handle, noepyWriteRGBA)

    # noesis.addOption(handle, "-shift", "<arg> is texture shift from the beginning of data block", noesis.OPTFLAG_WANTARG)
    # noesis.addOption(handle, "-size", "<arg> is size of texture in bytes", noesis.OPTFLAG_WANTARG)
    noesis.logPopup()
    return 1


# check if it's this type based on the data
def noepyCheckType(data):
    return WPGFile.is_valid_data(data)


def noepyLoadRGBA(data, tex_list):
    return WPGFile(tex_list, data=data).load()


class WPGFile:
    WPG_HEADER_SIZE = 32
    TGA_HEADER_SIZE = 18
    TGA_1BPP_HEADER_SIZE = 786

    @staticmethod
    def log(message, *args):
        print("[WPG]", message.format(*args))

    @staticmethod
    def is_valid_data(data):
        bs = NoeBitStream(data)
        bs.seek(0)
        header = bs.readBytes(WPGFile.WPG_HEADER_SIZE).decode('ascii').split('\0')[0]
        return header == "wpg"

    def __init__(self, tex_list, name=None, t_map=None, path=None, data=None):
        if name:
            self.name = name
        else:
            self.name = rapi.getLocalFileName(rapi.getInputName())

        self.map = t_map
        self.tex_list = tex_list
        self.count = 0
        self.bs = None

        if data:
            self.data = data
        elif path:
            with open(path, 'rb') as tex_file:
                self.data = tex_file
        else:
            self.log("[WPG] No input provided!")

        self.is_valid = WPGFile.is_valid_data(self.data)
        self.log("__init__: name={}, map={}, path={}, is_valid={}", self.name, self.map, path, self.is_valid)

    def load(self):
        self.log("***** load() function ******")

        if not self.is_valid:
            return 0

        if self.map:
            self.__load_from_map__()
        else:
            self.__load_from_bitstream__()

        self.log("Loaded {} textures", self.count)

        if self.count == 0:
            noesis.messagePrompt("[WPG] No textures were found in this file")

        return self.count

    def __load_from_bitstream__(self):
        self.bs = NoeBitStream(self.data)

        self.log("Not using map, reading with BitStream Data Size={}", self.bs.dataSize)
        cursor = self.WPG_HEADER_SIZE
        while cursor < self.bs.dataSize:
            tex, bpp = self.__load_sub__(cursor, self.bs.dataSize - cursor)

            if not tex:
                break

            if bpp == 1:
                header_size = self.TGA_1BPP_HEADER_SIZE
            else:
                header_size = self.TGA_HEADER_SIZE

            cursor += (tex.width * tex.height * bpp) + header_size

    def __load_from_map__(self):
        self.log("Loading using provided map")
        for x in self.map:
            self.__load_sub__(self.WPG_HEADER_SIZE + x['shift'], x['size'])

    def __load_sub__(self, start, size):
        self.log("Load_Sub: Start={}, Size={} ", start, size)

        # Read TGA from buffer
        self.bs.seek(start)
        buffer = self.bs.readBytes(size)
        tex = rapi.loadTexByHandler(buffer, '.tga')
        tex.name = "{0}.{1:02}.tga".format(self.name, self.count)

        if not tex:
            return 0, 0, 0

        # Check if it's 1BPP, 3BPP, or 4BPP
        # https://github.com/python-pillow/Pillow/blob/7aaf021822297a0c5aae258a9f68adfd2b590258/src/PIL/TgaImagePlugin.py
        self.bs.seek(start)
        tga_header = self.bs.readBytes(18)
        image_type = int.from_bytes(tga_header[2:4], byteorder='little')

        if image_type in (1, 9):
            bpp = 1
        elif image_type in (2, 10):
            if tex.pixelType == noesis.NOESISTEX_RGBA32:
                bpp = 4
            elif tex.pixelType == noesis.NOESISTEX_RGB24:
                bpp = 3
        else:
            bpp = 4
            self.log("Unsupported pixel type: {}", tex.pixelType)

        self.count += 1
        self.tex_list.append(tex)
        return tex, bpp
