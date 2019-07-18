import re
from enum import IntEnum
from typing import List

import numpy as np
from PIL import Image


class Const:
    DESCRIPTIONS = {
        'PROGRE': 'Progressive Scan text for TV',
        'TRIAL': 'Command Mission demo texts',
        'SUB_TXT': 'Weapon descriptions and pause menu',
        'SUB_TIT': 'Weapon and part names',
        'SAVE_TIT': 'Saving and loading',
        'RESULT': 'Result screen after each level',
        'PAL': 'Video mode settings',
        'OPT_TXT': 'Options menu',
        'OPT_TIT': 'Options menu control buttons names',
        'LABO_TXT': 'RD Lab Menu descriptions',
        'LABO_TIT': 'RD Lab Menu labels (Stage Select, Chip Dev...)',
        'HB_TIT': 'Stage, character, navigator, and netural armor descriptions',
        'HB_IM': 'Intermission descriptions',
        'HB_DM': 'Stage Select cutscenes',
        'CHIP_TIT': 'RD Chip names',
        'CHIP_TXT': 'RD Chip descriptions'
    }

    DESCRIPTION_MAP = {
        'NV1': "Alia's dialogue ",
        'NV2': "Layer's dialogue ",
        'NV3': "Palette's dialogue ",
        'DM_': "Dr. Light and other events ",
        'DM1': "X's dialogue ",
        'DM2': "Zero's dialogue ",
        'DM3': "Axl's dialogue ",
        'MOV': 'Pre-Rendered Video Subtitles ',
        'VA': "that involve Vile",
        'ST00': "in Noah's Park",
        'ST01': 'in Troia Base',
        'ST02': 'in Primrose',
        'ST03': 'in Pitch Black',
        'ST04': 'in Dynasty',
        'ST05': 'in Inferno',
        'ST06': 'in Central White',
        'ST07': 'in Metal Valley',
        'ST08': 'in Booster Forest',
        'ST09': 'in Jakob Elevator',
        'ST10': 'in Gateway',
        'ST11': "in Sigma's Palace",
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
        ['Serious', 'Surprised', 'Angry', 'Neutral Armor'],  # X
        ['Holding Sword', 'Serious', 'Eyes Closed'],  # Zero
        ['Smiling', 'Upset', 'Holding Gun', 'Serious'],  # Axl
        ['Speaking', 'Listening', 'Worried'],  # BG Alia
        ['Listening', 'Red Face', 'Slight Blush'],  # BG Layer
        ['Listening', 'Speaking', 'Thinking', 'RD Lab'],  # BG Pallette
        ['Serious'],  # Signas
        ['Hologram'],  # Dr. Light
        ['Default'],  # Optic Sunflower
        ['Default'],  # Gravity Antonion
        ['Default'],  # Dark Mantis
        ['Default'],  # Gigabolt Man-o-War
        ['Default'],  # Burn Rooster
        ['Default'],  # Avalanche Yeti
        ['Default'],  # Earthrock Trilobyte
        ['Default'],  # Bamboo Pandemonium
        ['Default'],  # Vile
        ['Copy', 'Real'],  # Sigma
        ['Regular', 'Psychopath Smirk', 'Defeated'],  # Lumine
        ['Speaking', 'Listening', 'Worried'],  # FG Alia
        ['Listening', 'Red Face', 'Slight Blush'],  # FG Layer
        ['Listening', 'Speaking', 'Thinking', 'RD Lab'],  # FG Pallette
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

    def read_int_array(self, size):
        arr = []
        for i in range(size):
            arr.append(self.read_int())
        return arr

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
        Bottom = 1
        Top = 0xFFFF

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
            return 'Invalid Mugshot : ' + str(mug_idx)
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

    def to_str_array(self, use_text=False):
        data = [self.voice, self.bgm, self.stop_bgm, self.camera_angle]
        data.extend(self.__raw_char_data)
        data.append(self.close_top)
        if use_text:
            data.append('Bot' if self.text_pos == 1 else 'Top')
            data.append(self.int18)
            data.append('Ye' if self.typing == 0 else 'No')
            data.append('Ye' if self.show_arrow == 1 else 'No')
        else:
            data.append(self.text_pos)
            data.append(self.int18)
            data.append(self.typing)
            data.append(self.show_arrow)

        data.append(self.char_mug_pos.name)

        for idx, num in enumerate(data):
            if num == 0xFFFF:
                data[idx] = '__'
            if num == 0xFFFE:
                data[idx] = 'FE'

            data[idx] = str(data[idx]).ljust(2)

        data[0].ljust(3)
        data[-1].ljust(6)

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

        self.characters = np.array(characters)

    def text_bytes_to_array(self, raw_bytes):
        sentences, max_sentence_len = self.__split_to_sentences__(raw_bytes)
        cols = 20 * max_sentence_len
        rows = 20 * len(sentences)
        im = np.zeros((rows, cols))
        for row_idx, sentence in enumerate(sentences):
            row_start = row_idx * 20
            row_end = row_start + 20
            for col_idx, char_byte in enumerate(sentence):
                if char_byte >= len(self.characters):
                    im_curr_char = self.characters[0]
                else:
                    im_curr_char = self.characters[char_byte]
                col_start = col_idx * 20
                col_end = col_start + 20
                im[row_start:row_end, col_start:col_end] = im_curr_char

        return im

    @staticmethod
    def __split_to_sentences__(raw_bytes):
        split_indices = [0]
        split_indices.extend([idx + 1 for idx, char_byte in enumerate(raw_bytes) if char_byte == 65533])
        split_indices.append(len(raw_bytes) + 1)
        sentences = []
        max_sentence_len = 0
        for split_idx, slice_start in enumerate(split_indices):
            if split_idx >= len(split_indices) - 1:
                break
            slice_end = split_indices[split_idx + 1]
            sentence = raw_bytes[slice_start:slice_end]
            max_sentence_len = max(max_sentence_len, len(sentence))
            sentences.append(sentence)
        return sentences, max_sentence_len


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
    def get_filename_description(fname: str):
        desc = Const.DESCRIPTIONS.get(fname)
        if desc is not None:
            return desc

        built_desc = ''
        for key in Const.DESCRIPTION_MAP.keys():
            if key in fname:
                built_desc += Const.DESCRIPTION_MAP[key]

        if built_desc == '':
            return 'Unknown File'
        return built_desc

    @staticmethod
    def convert_text_to_bytes(orig_text):
        text = orig_text.replace('\n', '[65533]')

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
            return '\n'
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

    @staticmethod
    def is_file(filename):
        filename = filename.replace('\x00', '')  # Remove padding zeros
        # Only allows a-z, A-Z, 0-9, and underscores (and filenames of length 10 and above)
        return len(filename) >= 10 and not bool(re.compile(r'[^a-zA-Z0-9_]').search(filename))

    def print(self):
        print('=== MCB Path:', self.path)
        if self.has_extras():
            print('IDX,VOI,BG,SM,CA,C1,M1,P1,C2,M2,P2,C3,M3,P3,C4,M4,P4,CT,TP,18,TY,AR,MugPos|||Text Message Goes Here***|||Filename')
            for idx, (extra, text_bytes) in enumerate(zip(self.extras, self.texts_raw)):
                text = self.convert_bytes_to_text(text_bytes).replace('\n', ' ')
                s_idx = str(idx).ljust(3)
                s_extra = ','.join(map(str, extra.to_str_array(False)))
                print('{},{}|||{}|||{}'.format(s_idx, s_extra, text, extra.filename))
        else:
            print('IDX|||Text')
            for idx, (text_bytes) in enumerate(self.texts_raw):
                text = self.convert_bytes_to_text(text_bytes).replace('\n', ' ')
                s_idx = str(idx).ljust(3)
                print('{}|||{}'.format(s_idx, text))

    def __init__(self, path=None):
        self.omcb_header = ''
        self.header = ''
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

        if len(self.omcb_header) > 0:
            writer.write_string(self.omcb_header)
            writer.write_int(self.size)
            writer.write_int(0)

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

    def has_extras(self):
        return len(self.files) != 0

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
        self.header = reader.read_string(16)

        # ARC File Check
        if 'OMCB' in self.header:
            reader.seek(0)
            self.omcb_header = reader.read_string(8)
            omcb_size = reader.read_int()  # Same as MCB size
            omcb_unused = reader.read_int()  # Seems to be 0
            self.header = reader.read_string(16)

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


def split3(arr):
    return [arr[0:128, 0:128], arr[128:257, 0:128], arr[0:128, 128:257]]


def split1(arr):
    return [arr]


def split2(arr):
    return [arr]


def split4(arr):
    return [arr[0:128, 0:128], arr[128:257, 0:128], arr[0:128, 128:257], arr[128:257, 128:257]]


if __name__ == '__main__':
    from pathlib import Path

    path = Path(r'C:\Users\xeroj\Desktop\Local_Programming\RockManX8_Tools\mugshots')
    npz_path = path / 'mugshots.npz'
    results = [
        split4(np.array(Image.open(path / 'X.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Zero.png'), dtype=np.uint8)),
        split4(np.array(Image.open(path / 'Axl.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Alia.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Layer.png'), dtype=np.uint8)),
        split4(np.array(Image.open(path / 'Pallette.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Signas.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Light.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Sunflower.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Antonion.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Mantis.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Man-o-War.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Rooster.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Yeti.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Trilobyte.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Pandamonium.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Vile.png'), dtype=np.uint8)),
        split2(np.array(Image.open(path / 'Sigma.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Lumine.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Alia.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Layer.png'), dtype=np.uint8)),
        split4(np.array(Image.open(path / 'Pallette.png'), dtype=np.uint8)),
    ]
    results = np.array(results, dtype=np.ndarray)
    np.savez_compressed(npz_path, mugshots=results)
    d = np.load(npz_path, allow_pickle=True)['mugshots']
    # mcb = MCBFile('C:/Users/xeroj/Desktop/Local_Programming/RockManX8_Tools/tools/arctool/LABO_TIT/X8/data/mes/USA/LABO_TIT.0589CBA3')
    # mcb.print()
