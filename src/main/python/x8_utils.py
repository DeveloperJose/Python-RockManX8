import re
from enum import IntEnum
from typing import List

import numpy as np
from PIL import Image


class Const:
    DESCRIPTIONS = {
        'PROGRE.mcb': 'Progressive Scan text for TV (PS2/USA folder only)',
        'TRIAL.mcb': 'Command Mission demo texts',
        'SUB_TXT.mcb': 'Weapon descriptions and pause menu',
        'SUB_TIT.mcb': 'Weapon and part names',
        'SAVE_TIT.mcb': 'Saving and loading',
        'RESULT.mcb': 'Result screen after each level',
        'PAL.mcb': 'Video mode settings',
        'OPT_TXT.mcb': 'Options menu',
        'OPT_TIT.mcb': 'Options menu control buttons names',
        'LABO_TXT.mcb': 'RD Lab Menu descriptions',
        'LABO_TIT.mcb': 'RD Lab Menu labels (Stage Select, Chip Dev...)',
        'HB_TIT.mcb': 'Stage/character/navigator/netural armor descriptions',
        'HB_IM.mcb': 'Intermissions',
        'HB_DM.mcb': 'Stage Select cutscenes',
        'CHIP_TIT.mcb': 'RD Chip names',
        'CHIP_TXT.mcb': 'RD Chip descriptions'
    }

    ALPHABET = [' ', '!', '"', '%', '&', '(', ')', 'x', '+', '-', ',',
                '.', '/', ':', ';', '=', '?', '@', '[', ']', '_', '~', '`', '°', '…', '…'
        , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        , 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                # 0x58, 59, 5A, 5B, 5C, 5D
        , "'", "||", "Σ", "◯", "△", "↑", '↓', '↙', '↘', '←', '→', '®', '€']

    CHARACTERS = ['X', 'Zero', 'Axl', 'BG Alia', 'BG Layer', 'BG Pallette', 'Signas', 'Dr. Light', 'Optic Sunflower', 'Gravity Antonion', 'Dark Mantis',
                  'Gigabolt Man-o-War', 'Burn Rooster', 'Avalanche Yeti', 'Earthrock Trilobyte', 'Bamboo Pandemonium', 'Vile', 'Sigma', 'Lumine', 'FG Alia',
                  'FG Layer', 'FG Pallette', 'None']

    # http://sprites-inc.co.uk/sprite.php?local=X/X8/Mugshots/
    MUGSHOT_DESCRIPTIONS = [
        ['Normal R', 'Surprised F', 'Angry R', 'Neutral Armor F'],  # X
        ['Normal Holding Sword F', 'Serious R', 'Eyes Closed R'],  # Zero
        ['Smiling F', 'Upset R', 'Holding Gun R', 'Serious F'],  # Axl
        ['Mic Hold L', 'Headphone Hold L', 'Worried F'],  # BG Alia
        ['Headphone Hold L', 'Blush F', 'Embarrassed F'],  # BG Layer
        ['Headphone Hold L', 'Mic Hold L', 'Thinking L', 'RD Lab F'],  # BG Pallette
        ['Regular L'],  # ??
        ['Hologram L'],  # Dr. Light
        ['Regular L'],  # Optic Sunflower
        ['Regular L'],  # Gravity Antonion
        ['Regular L'],  # Dark Mantis
        ['Regular L'],  # Gigabolt Man-o-War
        ['Regular L'],  # Burn Rooster
        ['Regular L'],  # Avalanche Yeti
        ['Regular L'],  # Earthrock Trilobyte
        ['Regular L'],  # Bamboo Pandemonium
        ['Regular L'],  # Vile
        ['Copy L', 'Real F'],  # Sigma
        ['Regular F', 'Smirk F', 'Defeat F'],  # Lumine
        ['Mic Hold L', 'Headphone Hold L', 'Worried F'],  # FG Alia
        ['Headphone Hold L', 'Blush F', 'Embarrassed F'],  # FG Layer
        ['Headphone Hold L', 'Mic Hold L', 'Thinking L', 'RD Lab F'],  # FG Pallette
        ['None'],  # None or Sigma?
    ]


class FileStream:
    def __init__(self, file):
        self.file = file

    def read_string(self, size=16):
        raw = self.file.read(size)
        return raw.decode('utf-8', errors='replace')

    def read_int(self, size=2):
        raw = self.file.read(size)
        return int.from_bytes(raw, byteorder='little')

    def tell(self):
        return self.file.tell()

    def seek(self, offset):
        self.file.seek(offset)

    def write_string(self, s):
        str_bytes = str.encode(s)
        self.file.write(str_bytes)

    def write_int(self, i):
        int_bytes = i.to_bytes(2, byteorder='little')
        self.file.write(int_bytes)

    def write_string_array(self, arr):
        for s in arr:
            self.write_string(s)

    def write_int_array(self, arr):
        for i in arr:
            self.write_int(i)


class MCBExtra:
    class MugshotPosition(IntEnum):
        Left = 0
        Right = 1

    class TextPosition(IntEnum):
        Bottom = 0xFFFF
        Top = 1

    @property
    def char_mug_description(self):
        return self.get_mugshot_description(self.char, self.char_mug)

    @property
    def char_description(self):
        return self.get_character_description(self.char)

    def __init__(self):
        self.voice = 0xFFFF
        self.bgm = 0xFFFF
        self.stop_bgm = 0xFFFF
        self.camera_angle = 0xFFFF
        self.char = 0xFFFF
        self.char_mug = 0xFFFF
        self.char_pos = 0xFFFF
        self.close_top = 0xFFFF
        self.text_pos = 0xFFFF
        self.int18 = 0xFFFF
        self.typing = 0xFFFF
        self.show_arrow = 0xFFFF

        self.__raw_char_data = [0xFFFF] * 12
        self.char_mug_pos = self.MugshotPosition(0)
        self.filename = ''

    @classmethod
    def from_reader(cls, reader):
        instnc = cls()
        instnc.voice = reader.read_int()
        instnc.bgm = reader.read_int()
        instnc.stop_bgm = reader.read_int()  # Stops BGM from playing when set to 0
        instnc.camera_angle = reader.read_int()  # [1-3] camera angles, only used for boss interactions

        char1 = reader.read_int()
        char_mug1 = reader.read_int()
        char_pos1 = reader.read_int()  # Seems to be unused, mostly 0, sometimes 1, 0xFFFF for the weird case
        char2 = reader.read_int()
        char_mug2 = reader.read_int()
        char_pos2 = reader.read_int()
        char3 = reader.read_int()
        char_mug3 = reader.read_int()
        char_pos3 = reader.read_int()
        char4 = reader.read_int()
        char_mug4 = reader.read_int()
        char_pos4 = reader.read_int()
        char_data = [char1, char_mug1, char_pos1, char2, char_mug2, char_pos2, char3, char_mug3, char_pos3, char4, char_mug4, char_pos4]

        # Figure out which of the 4 char/image/pos pairs is the one used for this extra
        # Moves range of possible [0,1,2,3] to range of char_idx [0,3,6,9]
        # [TopLeft,TopRight,BottomLeft,BottomRight]
        possible = [char1, char2, char3, char4]
        pair_idx = possible.index(min(possible))
        char_idx = pair_idx * 3
        instnc.char = char_data[char_idx]
        instnc.char_mug = char_data[char_idx + 1]
        instnc.char_pos = char_data[char_idx + 2]
        instnc.__raw_char_data = char_data

        # Figure out where the portrait and box are drawn
        # [Left=0,Right=1,Left=2,Right=3] so idx mod 2 will get the right pattern
        instnc.char_mug_pos = MCBExtra.MugshotPosition(pair_idx % 2)

        # Closes the top dialogue box when set to 0 (and when it does, char2 is 0xFFFE for some reason)
        # It's set to 1 when the dialogue box is top as well
        instnc.close_top = reader.read_int()

        instnc.text_pos = reader.read_int()  # 1 for bottom, anything else for top (usually 0xFFFF I think)
        instnc.int18 = reader.read_int()  # Always 0xFFFF
        instnc.typing = reader.read_int()  # 0 if typing one letter at a time
        instnc.show_arrow = reader.read_int()  # 1 if showing an arrow, 2 otherwise
        return instnc

    @staticmethod
    def is_valid_char(char_idx):
        return 0 <= char_idx < len(Const.CHARACTERS)

    @staticmethod
    def get_mugshot_description(char_idx, mug_idx):
        if not MCBExtra.is_valid_char(char_idx):
            return 'Invalid Mugshot Character'

        mugshots = Const.MUGSHOT_DESCRIPTIONS[char_idx]
        is_valid_mugshot = (0 <= mug_idx < len(mugshots))
        if not is_valid_mugshot:
            return 'Invalid Mugshot'
        return mugshots[mug_idx]

    @staticmethod
    def get_character_description(char_idx):
        if not MCBExtra.is_valid_char(char_idx):
            return 'Invalid Character'
        return Const.CHARACTERS[char_idx]

    def __create_char_data__(self):
        char_data = [0xFFFF] * 12

        is_top = (self.text_pos == MCBExtra.TextPosition.Top)
        is_left = (self.char_mug_pos == MCBExtra.MugshotPosition.Left)
        if is_top:
            if is_left:
                idxs = slice(0, 3)
            else:
                idxs = slice(3, 6)
        else:
            if is_left:
                idxs = slice(6, 9)
            else:
                idxs = slice(9, 12)

        char_data[idxs] = [self.char, self.char_mug, self.char_pos]

        return char_data

    def to_byte_array(self):
        data = [self.voice, self.bgm, self.stop_bgm, self.camera_angle]
        data.extend(self.__create_char_data__())
        data.extend([self.close_top, self.text_pos, self.int18, self.typing, self.show_arrow])
        return data

    def to_str_array(self):
        data = [self.voice, self.bgm, self.stop_bgm, self.camera_angle]
        data.extend(self.__raw_char_data)
        data.append(self.close_top)
        data.append('Bot' if self.text_pos == 1 else 'Top')
        data.append(self.int18)
        data.append('Ye' if self.typing == 0 else 'No')
        data.append(str(self.show_arrow).ljust(2))
        data.append(self.char_mug_pos.name.ljust(6))

        for idx, num in enumerate(data):
            if num == 0xFFFF:
                data[idx] = '__'
            if num == 0xFFFE:
                data[idx] = 'FE'

            data[idx] = str(data[idx]).ljust(2)

        data[0] = str(data[0]).ljust(3)

        return data


class Font:
    def __init__(self, path):
        self.wpg = WPGFile(path)

        characters = []
        for texture in self.wpg.textures:
            # Extract all 144 characters from the texture
            for row in range(12):
                for col in range(12):
                    rstart = row * 20
                    rend = rstart + 20
                    cstart = col * 20
                    cend = cstart + 20
                    im_char = texture[rstart:rend, cstart:cend]
                    characters.append(im_char)

        self.characters = characters


class WPGFile:
    def __init__(self, path=None):
        self.textures = None
        self.path = None

        if path is not None:
            self.path = path
            self.__load_from_file__(path)

    def __load_from_file__(self, path):
        textures = []
        with open(path, 'rb') as file:
            file.seek(0)
            wpg_header = file.read(32)
            while True:
                texture_data = file.read(262162)
                # Check for end of file
                if len(texture_data) != 262162:
                    break

                # Read texture
                im_raw = Image.frombytes('RGBA', (256, 256), texture_data)
                im_raw_gray = im_raw.convert("L")
                im_texture = np.array(im_raw_gray)[:240, :240]
                textures.append(im_texture)

        self.textures = textures


class MCBFile:
    extras: List[MCBExtra]

    LENGTH_HEADER = 16
    LENGTH_FILENAME_EXTRA = 42
    LENGTH_INTEGER = 2
    LENGTH_STRING = 16

    @staticmethod
    def get_filename_description(fname):
        desc = Const.DESCRIPTIONS.get(fname)
        if desc is None:
            desc = 'Unknown File'
        return desc

    @staticmethod
    def convert_text_to_bytes(orig_text):
        text = orig_text.replace('[newline]', '[65533]')

        raw_bytes = []
        current_stack = ''
        reading_byte = False
        for char in text:
            if reading_byte:
                if char == ']':
                    try:
                        stack_bytes = int(current_stack)
                    except ValueError:
                        stack_bytes = 0
                    raw_bytes.append(stack_bytes)
                    reading_byte = False
                    current_stack = ''
                else:
                    current_stack += char
            elif char == '[':
                reading_byte = True
            else:
                char_byte = MCBFile.char_to_byte(char)
                raw_bytes.append(char_byte)

        if len(raw_bytes) == 0:
            raw_bytes = [0]

        return raw_bytes

    @staticmethod
    def byte_to_str(b):
        if b == 65533:
            return '[newline]'
        elif b < 0 or b >= len(Const.ALPHABET):
            return '[{}]'.format(b)
        else:
            return Const.ALPHABET[b]

    @staticmethod
    def char_to_byte(st):
        try:
            return Const.ALPHABET.index(st)
        except ValueError:
            return 0

    @staticmethod
    def convert_bytes_to_text(raw_bytes):
        text = ''
        for text_byte in raw_bytes:
            text += MCBFile.byte_to_str(text_byte)
        return text

    def print(self):
        if self.has_extras():
            print('=== MCB Path:', self.path)
            print('IDX,VOI,BG,I2,I3,C1,M1,P1,C2,M2,P2,C3,M3,P3,C4,M4,P4,16,TPO,18,TY,AR,MugPos|||Text Message Goes Here***|||Filename')
            for idx, (extra, text_bytes) in enumerate(zip(self.extras, self.texts_raw)):
                text = self.convert_bytes_to_text(text_bytes)
                s_idx = str(idx).ljust(3)
                s_extra = ','.join(map(str, extra.to_str_array()))
                print('{},{}|||{}|||{}'.format(s_idx, s_extra, text, extra.filename))
        else:
            print('IDX|||Text')
            for idx, (text_bytes) in enumerate(self.texts_raw):
                text = self.convert_bytes_to_text(text_bytes)
                s_idx = str(idx).ljust(3)
                print('{}|||{}'.format(s_idx, text))

    def __init__(self, path=None):
        self.header = ""
        self.size = 0
        self.text_count = 0
        self.offsets = []
        self.files = []
        self.texts_raw = []
        self.extras = []

        self.seek_offset_end = 0
        self.seek_text_start = 0

        if path is not None:
            self.path = path
            self.__load_from_file__(path)

    def save(self, spath=None):
        self.__recalculate__()
        if spath is None:
            spath = self.path

        file = open(spath, 'wb')
        writer = FileStream(file)

        writer.write_string(self.header)
        writer.write_int(self.size)
        writer.write_int(self.text_count)
        writer.write_int_array(self.offsets)
        writer.write_string_array(self.files)

        for idx, text_bytes in enumerate(self.texts_raw):
            if self.has_extras():
                extra_bytes = self.extras[idx].to_byte_array()
                writer.write_int_array(extra_bytes)
            writer.write_int_array(text_bytes)
            writer.write_int(0xFFFF)

        file.close()

    @staticmethod
    def is_file(filename):
        filename = filename.replace('\x00', '')  # Remove padding zeros
        # Only allows a-z, A-Z, 0-9, and underscores (and filenames of length 10 and above)
        return len(filename) >= 10 and not bool(re.compile(r'[^a-zA-Z0-9_]').search(filename))

    def has_extras(self):
        return len(self.files) != 0

    def edit_text(self, idx, new_text):
        # Convert new_text to bytes
        text_bytes = []
        for char in new_text:
            try:
                char_byte = Const.ALPHABET.index(char)
            except ValueError:
                char_byte = 0

            text_bytes.append(char_byte)

        self.texts_raw[idx] = text_bytes
        self.__recalculate__()

    def __load_from_file__(self, path):
        file = open(path, 'rb')
        reader = FileStream(file)

        self.__load_header__(reader)
        self.__load_files__(reader)
        self.__load_texts__(reader)

        file.close()

    def __recalculate__(self):
        # Recalculate size (Header (16) + Size (2) + Text Count (2)
        self.size = self.LENGTH_STRING + self.LENGTH_INTEGER + self.LENGTH_INTEGER \
                    + len(self.offsets) * self.LENGTH_INTEGER \
                    + len(self.files) * self.LENGTH_STRING \
                    + sum(len(x) + 1 for x in self.texts_raw) * self.LENGTH_INTEGER \
                    + len(self.extras) * self.LENGTH_FILENAME_EXTRA

        # Recalculate offsets
        offset = 0
        for idx, txt in enumerate(self.texts_raw):
            self.offsets[idx] = offset
            if self.has_extras():
                offset += self.LENGTH_FILENAME_EXTRA
            # Take into consideration FF terminator (+1)
            offset += (len(txt) + 1) * 2

        self.text_count = len(self.texts_raw)

    def __load_header__(self, reader):
        self.header = reader.read_string(self.LENGTH_HEADER)
        self.size = reader.read_int()
        self.text_count = reader.read_int()
        for i in range(self.text_count):
            offset = reader.read_int()
            self.offsets.append(offset)

        self.seek_offset_end = reader.tell()

    def __load_files__(self, reader):
        filename = reader.read_string()
        while self.is_file(filename):
            self.files.append(filename)
            filename = reader.read_string()

    def __load_texts__(self, reader):
        self.seek_text_start = self.seek_offset_end
        if len(self.files) > 0:
            # Skip all the filenames and the first extra block
            self.seek_text_start = self.seek_offset_end + (16 * len(self.files)) + 42

        for i in range(self.text_count):
            offset = self.seek_text_start + self.offsets[i]
            offset_extras = offset - self.LENGTH_FILENAME_EXTRA
            reader.seek(offset)

            text_raw = []
            data = reader.read_int()
            while data != 65535:
                text_raw.append(data)
                data = reader.read_int()

            self.texts_raw.append(text_raw)

            if self.has_extras():
                reader.seek(offset_extras)
                extra = MCBExtra.from_reader(reader)
                extra.filename = self.files[i]
                self.extras.append(extra)


if __name__ == '__main__':
    mcb = MCBFile('mes/SPA/LABO_TIT.mcb')
    mcb.print()
    mcb.save('TEST.mcb')