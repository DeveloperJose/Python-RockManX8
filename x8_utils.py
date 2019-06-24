# Author: Jose G. Perez <josegperez@mail.com>
# Utilities for editing Mega Man X8 files
# So far, only text editing is implemented (but it's fully functional!)

# Extracted from game and from opk/title/spa/FONT.wsx
alphabet = [' ', '!', '"', '%', '&', '(', ')', 'x', '+', '-', ',',
            '.', '/', ':', ';', '=', '?', '@', '[', ']', '_', '~', '`', '°', '…', '…'
            , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            , 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
            , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
            # 0x58, 59, 5A, 5B, 5C, 5D
            , "'", "||", "Σ", "◯", "△", "↑", '↓', '↙', '↘', '←', '→', '®', '€']

def byte_to_str(idx):
    if idx == 65533:
        # return ' \n\t'
        return ' '
    elif idx < 0 or idx >= len(alphabet):
        return '_'
    else:
        return alphabet[idx]


class FileReaderWriter():
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


class MCBExtra():
    from enum import IntEnum
    class DBoxPosition(IntEnum):
        TopLeft = 0
        TopRight = 1
        BottomLeft = 2
        BottomRight = 3

    # http://sprites-inc.co.uk/sprite.php?local=X/X8/Mugshots/
    CHARACTERS = ['X', 'Zero', 'Axl', 'BG Alia', 'BG Layer', 'BG Pallette', 'Signas', 'Dr. Light', 'Optic Sunflower', 'Gravity Antonion', 'Dark Mantis',
                  'Gigabolt Man-o-War', 'Burn Rooster', 'Avalanche Yeti', 'Earthrock Trilobyte', 'Bamboo Pandemonium', 'Vile', 'Sigma', 'Lumine', 'FG Alia',
                  'FG Layer', 'FG Pallette', 'None']

    MUGSHOTS = [
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
        ['Copy L', 'Real F'],  # Sigma2
    ]

    @classmethod
    def get_mugshot(cls, int_char, int_mug):
        if int_char == 0xFFFF:
            return 'None'

        int_mug -= 1
        if int_char < 0 or int_char >= len(MCBExtra.CHARACTERS):
            return 'Invalid: ' + str(int_char)

        mugshots = cls.MUGSHOTS[int_char]

        # Pose 0 defaults to the first pose
        # Get pose string if possible
        if int_mug < 0 or int_mug >= len(mugshots):
            return 'Default: ' + mugshots[0]
        return mugshots[int_mug]

    @classmethod
    def get_character(cls, int_char):
        if int_char == 0xFFFF:
            return 'None'
        elif int_char < 0 or int_char >= len(cls.CHARACTERS):
            return 'Invalid: ' + str(int_char)
        else:
            return cls.CHARACTERS[int_char]

    @classmethod
    def from_reader(cls, reader):
        instnc = cls()
        instnc.voice = reader.read_int()
        instnc.bgm = reader.read_int()
        instnc.int2 = reader.read_int()  # Stops BGM from playing when set to 0
        instnc.int3 = reader.read_int()  # [1-3] camera angles, only used for boss interactions

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
        possible = [char1, char2, char3, char4]
        pair_idx = possible.index(min(possible))
        char_idx = pair_idx * 3
        instnc.char = char_data[char_idx]
        instnc.char_mug = char_data[char_idx+1]
        instnc.char_pos = char_data[char_idx+2]
        instnc.__raw_char_data = char_data

        # Figure out where the portrait and box are drawn
        instnc.char_box = instnc.DBoxPosition(pair_idx)

        # Closes the top dialogue box when set to 0 (and when it does, char2 is 0xFFFE for some reason)
        # It's set to 1 when the dialogue box is top as well
        instnc.int16 = reader.read_int()

        instnc.text_pos = reader.read_int()
        instnc.int18 = reader.read_int()  # Always 0xFFFF
        instnc.typing = reader.read_int()
        instnc.show_arrow = reader.read_int()
        return instnc

    def __init__(self):
        self.voice = 0xFFFF
        self.bgm = 0xFFFF
        self.int2 = 0xFFFF
        self.int3 = 0xFFFF
        self.char = 0xFFFF
        self.char_mug = 0xFFFF
        self.char_pos = 0xFFFF
        self.char_box = self.DBoxPosition(0)
        self.int16 = 0xFFFF
        self.text_pos = 0xFFFF
        self.int18 = 0xFFFF
        self.typing = 0xFFFF
        self.show_arrow = 0xFFFF

    def __create_char_data__(self):
        char_data = [0xFFFF] * 12

        if self.char_box == self.DBoxPosition.TopLeft:
            idxs = slice(0,3)
        elif self.char_box == self.DBoxPosition.TopRight:
            idxs = slice(3,6)
        elif self.char_box == self.DBoxPosition.BottomLeft:
            idxs = slice(6,9)
        else:
            idxs = slice(9,12)

        char_data[idxs] = [self.char, self.char_mug, self.char_pos]

        return char_data

    def to_array(self):
        data = [self.voice, self.bgm, self.int2, self.int3]
        data.extend(self.__create_char_data__())
        data.extend([self.int16, self.text_pos, self.int18, self.typing, self.show_arrow])
        return data

    def to_array2(self):
        data = [self.voice, self.bgm, self.int2, self.int3]
        data.extend(self.__raw_char_data)
        data.append(self.int16)
        data.append('Dn' if self.text_pos == 1 else 'Up')
        data.append(self.int18)
        data.append('Ye' if self.typing == 0 else 'No')
        data.append('Ye' if self.show_arrow == 1 else 'No')
        data.append(self.char_box.name.ljust(10))

        for idx, num in enumerate(data):
            if num == 0xFFFF:
                data[idx] = '__'
            if num == 0xFFFE:
                data[idx] = 'FE'

            data[idx] = str(data[idx]).ljust(2)

        data[0] = str(data[0]).ljust(3)

        return data

    def __str__(self):
        f_char = MCBExtra.get_character(self.char)
        f_mug = MCBExtra.get_mugshot(self.char, self.char_mug)
        f_char_pos = self.char_pos
        f_voice = self.voice
        f_bgm = self.bgm
        f_text_pos = 'Down' if self.text_pos == 1 else 'Up'
        f_typing = 'Y' if self.typing == 0 else 'N'
        f_show_arrow = 'Y' if self.show_arrow == 1 else 'S' if self.show_arrow == 2 else 'N'

        frmt = "{C:%s,MUG:%s,CPOS:%d,V:%d,BGM:%d,TPOS:%s,TYP:%s,ARR:%s}"
        frmt = frmt % (f_char, f_mug, f_char_pos, f_voice, f_bgm, f_text_pos, f_typing, f_show_arrow)
        return frmt

class MCBFile():
    LENGTH_HEADER = 16
    LENGTH_FILENAME_EXTRA = 42
    LENGTH_INTEGER = 2
    LENGTH_STRING = 16

    @property
    def texts(self):
        texts = []
        for text_raw in self.texts_raw:
            text = ''
            for text_byte in text_raw:
                text += byte_to_str(text_byte)
            texts.append(text)

        return texts

    def print(self):
        if self.has_extras():
            print('=== MCB Path:', self.path)
            print('IDX,VOI,BG,I2,I3,C1,M1,P1,C2,M2,P2,C3,M3,P3,C4,M4,P4,16,TP,18,TY,AR,CB        |||Text Message Goes Here***|||Filename')
            for idx, (extra, text, filename) in enumerate(zip(self.extras, self.texts, self.files)):
                s_idx = str(idx).ljust(3)
                s_extra = ','.join(map(str, extra.to_array2()))
                print('{},{}|||{}|||{}'.format(s_idx, s_extra, text, filename))
        else:
            print('IDX|||Text')
            for idx, (text) in enumerate(self.texts):
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
        if spath is None:
            spath = self.path
        file = open(spath, 'wb')
        writer = FileReaderWriter(file)

        writer.write_string(self.header)
        writer.write_int(self.size)
        writer.write_int(self.text_count)
        writer.write_int_array(self.offsets)
        writer.write_string_array(self.files)

        for idx, (text_bytes, extra) in enumerate(zip(self.texts_raw, self.extras)):
            extra_bytes = extra.to_array()
            writer.write_int_array(extra_bytes)
            writer.write_int_array(text_bytes)
            writer.write_int(0xFFFF)

        file.close()

    def is_file(self, filename):
        import re
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
                char_byte = alphabet.index(char)
            except ValueError:
                char_byte = 0

            text_bytes.append(char_byte)

        self.texts_raw[idx] = text_bytes
        self.__recalculate__()

    def __load_from_file__(self, path):
        file = open(path, 'rb')
        reader = FileReaderWriter(file)

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
            text = ''
            data = reader.read_int()
            while data != 65535:
                text_raw.append(data)
                data = reader.read_int()

            self.texts_raw.append(text_raw)

            if self.has_extras():
                reader.seek(offset_extras)
                extra = MCBExtra.from_reader(reader)
                self.extras.append(extra)


if __name__ == '__main__':
    # reset_mcb()
    mcb_en = MCBFile('mes/ENG/HB_DM.mcb')
    mcb_en.save('mes/SPA/HB_DM.mcb')
    mcb = MCBFile('mes/SPA/HB_DM.mcb')
    mcb.print()

    # import os
    # for fname in os.listdir("mes/ENG/"):
    #     print("=============== File:", 'mes/ENG/'+fname)
    #     mcb = MCBFile("mes/ENG/" + fname)
    #     if mcb.has_extras():
    #         head = 'IDX,VOI,BG,I2,I3,C1,M1,P1,C2,M2,P2,C3,M3,P3,C4,M4,P4,16,TP,18,TY,AR|||Text Message'
    #         print(head)
    #         for id in range(len(mcb.texts)):
    #             print(str(id).ljust(3) + ',' + ','.join(map(str, mcb.extras[id].to_array2())) + '|||' + mcb.texts[id])
    #         print(head)
            # for text, extra in zip(mcb.texts, mcb.extras):
            #     if extra.char_pos != 0:
            #         print(text)
            #         print(extra)
            #         print()
    #
    # mcb = MCBFile('mes/SPA/HB_DM.mcb')
    # head = 'IDX,VOI,BG,I2,I3,C1,M1,P1,C2,M2,P2,C3,M3,P3,C4,M4,P4,16,TP,18,TY,AR|||Text Message'
    # print(head)
    # for id in range(len(mcb.texts)):
    #     print(str(id).ljust(3) + ',' + ','.join(map(str, mcb.extras[id].to_array2())) + '|||' + mcb.texts[id])
    # print(head)