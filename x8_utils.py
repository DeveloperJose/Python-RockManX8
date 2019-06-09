# Extracted from game and from opk/title/spa/FONT.wsx
alphabet = [' ', '!', '"', '%', '&', '(', ')', 'x', '+', '-', ',',
            '.', '/', ':', ';', '=', '?', '@', '[', ']', '_', '~', '`', '°', '…', '…'
            , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            , 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
            , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
            # 0x58, 59, 5A, 5B, 5C, 5D
            , "'", "||", "Σ", "◯", "△", "↑", '↓', '↙', '↘', '←', '→', '®', '€']

# http://sprites-inc.co.uk/sprite.php?local=X/X8/Mugshots/
poses = [
    ['Normal R', 'Surprised F', 'Angry R', 'Neutral Armor F'] , # X
    ['Normal Holding Sword F', 'Serious R', 'Eyes Closed R'], # Zero
    ['Smiling F', 'Upset R', 'Holding Gun R', 'Serious F'], # Axl
    ['Mic Hold L', 'Headphone Hold L', 'Worried F'], # Alia
    ['Headphone Hold L', 'Blush F', 'Embarrassed F'], # Layer
    ['Headphone Hold L', 'Mic Hold L', 'Thinking L', 'RD Lab F'], # Pallette
    ['Regular L'], # ??
    ['Hologram L'], # Dr. Light
    ['Regular L'], # Optic Sunflower
    ['Regular L'], # Gravity Antonion
    ['Regular L'], # Dark Mantis
    ['Regular L'], # Gigabolt Man-o-War
    ['Regular L'], # Burn Rooster
    ['Regular L'], # Avalanche Yeti
    ['Regular L'], # Earthrock Trilobyte
    ['Regular L'], # Bamboo Pandemonium
    ['Regular L'], # Vile
    ['Copy L', 'Real F'], # Sigma
    ['Regular F', 'Smirk F', 'Defeat F'], # Lumine
]

characters = ['X', 'Zero', 'Axl', 'BG Alia', 'BG Layer', 'BG Pallette', 'Signas', 'Dr. Light', \
              'Optic Sunflower', 'Gravity Antonion' ,'Dark Mantis', 'Gigabolt Man-o-War', 'Burn Rooster', \
              'Avalanche Yeti' ,'Earthrock Trilobyte' ,'Bamboo Pandemonium' ,'Vile' , \
              'Sigma', 'Lumine', 'FG Alia', 'FG Layer', 'FG Pallette', 'None']

def get_pose(char_idx, pose_idx):
    pose_idx -= 1
    # Navigator and Sigma FG/BG shenanigans
    if char_idx == 19:
        char_idx = 3
    elif char_idx == 20:
        char_idx = 4
    elif char_idx == 21:
        char_idx = 5
    elif char_idx == 22:
        char_idx = 17

    if char_idx < 0 or char_idx >= len(characters):
        return 'Invalid Character: ' + str(char_idx)
    char_poses = poses[char_idx]

    # Pose 0 defaults to the first pose
    # Get pose string if possible
    if pose_idx < 0 or pose_idx >= len(char_poses):
        return 'OFB: ' + char_poses[0]
    return char_poses[pose_idx]

def get_character(idx):
    if idx < 0 or idx >= len(characters):
        return 'Unknown: ' + str(idx)
    else:
        return characters[idx]

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

    def read_int(self):
        raw = self.file.read(2)
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

class MCBFile():
    LENGTH_HEADER = 16
    LENGTH_FILENAME_EXTRA = 42
    LENGTH_INTEGER = 2
    LENGTH_STRING = 16

    def __init__(self, path=None):
        self.header = ""
        self.size = 0
        self.text_count = 0
        self.offsets = []
        self.files = []
        self.texts_raw = []
        self.texts = []
        self.extras_raw = []
        self.extras = []

        self.seek_offset_end = 0
        self.seek_text_start = 0

        if path is not None:
            self.load_from_file(path)

    def edit_text(self, idx, new_text):
        # Convert new_text to bytes
        text_bytes = []
        for char in new_text:
            try:
                char_byte = alphabet.index(char)
            except ValueError:
                char_byte = 0

            text_bytes.append(char_byte)

        self.texts[idx] = new_text
        self.texts_raw[idx] = text_bytes
        self.recalculate()

    def recalculate(self):
        # Recalculate size (Header (16) + Size (2) + Text Count (2)
        self.size = self.LENGTH_STRING + self.LENGTH_INTEGER + self.LENGTH_INTEGER \
                    + len(self.offsets) * self.LENGTH_INTEGER \
                    + len(self.files) * self.LENGTH_STRING \
                    + sum(len(x)+1 for x in self.texts) * self.LENGTH_INTEGER \
                    + len(self.extras) * self.LENGTH_FILENAME_EXTRA

        # Recalculate offsets
        offset = 0
        for idx, txt in enumerate(self.texts_raw):
            self.offsets[idx] = offset
            offset += (len(txt) + 1) * 2

        self.text_count = len(self.texts)

    def save(self, path):
        file = open(path, 'wb')
        writer = FileReaderWriter(file)

        writer.write_string(self.header)
        writer.write_int(self.size)
        writer.write_int(self.text_count)
        writer.write_int_array(self.offsets)
        writer.write_string_array(self.files)

        for idx, text_bytes in enumerate(self.texts_raw):
            extra_bytes = self.extras_raw[idx]
            writer.write_int_array(extra_bytes)
            writer.write_int_array(text_bytes)
            writer.write_int(0xFFFF)

        file.close()

    def load_from_file(self, path):
        file = open(path, 'rb')
        reader = FileReaderWriter(file)

        self.__load_header__(reader)
        self.__load_files__(reader)
        self.__load_text__(reader)

        file.close()

    def is_file(self, str):
        return str[0:2] in ['NV', 'HB'] or str[0:3] in ['SUB', 'OPT'] or str[0:4] in ['DEMO', 'MENU', 'CHIP'] or str[0:6] in ['RESULT']

    def has_extras(self):
        return len(self.files) != 0

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

    def __load_text__(self, reader):
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
                text += byte_to_str(data)
                data = reader.read_int()

            self.texts_raw.append(text_raw)
            self.texts.append(text)

            if self.has_extras():
                self.__load_extra__(reader, offset_extras)

    def __load_extra__(self, reader, offset):
        extra_raw = []
        extra = []
        reader.seek(offset)
        idx_voice = reader.read_int()
        idx_bgm = reader.read_int()
        idx1 = reader.read_int()
        idx2 = reader.read_int()
        idx_char1 = reader.read_int()
        idx_pose1 = reader.read_int()
        idx5 = reader.read_int()
        idx_char2 = reader.read_int()
        idx_pose2 = reader.read_int()
        idx8 = reader.read_int()
        idx_char3 = reader.read_int()
        idx_pose3 = reader.read_int()
        idx11 = reader.read_int()
        idx_char4 = reader.read_int()
        idx_pose4 = reader.read_int()
        idx14 = reader.read_int()
        idx15 = reader.read_int()
        idx_text_pos = reader.read_int()
        idx17 = reader.read_int()
        idx_typing = reader.read_int()
        idx_show_arrow = reader.read_int()

        extra_raw.append(idx_voice)
        extra_raw.append(idx_bgm)
        extra_raw.append(idx1)
        extra_raw.append(idx2)
        extra_raw.append(idx_char1)
        extra_raw.append(idx_pose1)
        extra_raw.append(idx5)
        extra_raw.append(idx_char2)
        extra_raw.append(idx_pose2)
        extra_raw.append(idx8)
        extra_raw.append(idx_char3)
        extra_raw.append(idx_pose3)
        extra_raw.append(idx11)
        extra_raw.append(idx_char4)
        extra_raw.append(idx_pose4)
        extra_raw.append(idx14)
        extra_raw.append(idx15)
        extra_raw.append(idx_text_pos)
        extra_raw.append(idx17)
        extra_raw.append(idx_typing)
        extra_raw.append(idx_show_arrow)


        count = 0
        idx_char = -1
        idx_pose = -1
        if idx_char1 < len(characters):
            idx_char = idx_char1
            idx_pose = idx_pose1
            count += 1
        if idx_char2 < len(characters):
            idx_char = idx_char2
            idx_pose = idx_pose2
            count += 1
        if idx_char3 < len(characters):
            idx_char = idx_char3
            idx_pose = idx_pose3
            count += 1
        if idx_char4 < len(characters):
            idx_char = idx_char4
            idx_pose = idx_pose4
            count += 1

        if count > 1:
            print(idx_char1, idx_char2, idx_char3, idx_char4)
            import pdb
            pdb.set_trace()

        extra.append("{Char:}" + get_character(idx_char))
        extra.append("{Pose:}" + get_pose(idx_char, idx_pose))
        extra.append("{Voice:"+str(idx_voice)+"}")
        extra.append("{BGM:"+str(idx_bgm)+"}")
        extra.append("{TextPo:" + str(idx_text_pos) + "}")
        extra.append("{Typing:"+str(idx_typing)+"}")
        extra.append("{Arrow:"+str(idx_show_arrow)+"}")

        self.extras_raw.append(extra_raw)
        self.extras.append(extra)

if __name__ == '__main__':
    mcb = MCBFile('mes/SPA/LABO_TXT.mcb')
    # import os
    # for fname in os.listdir("mes/USA/"):
    #     print("===== File:", fname)
    #     mcb = MCBFile("mes/USA/" + fname)
    #     for idx, text in enumerate(mcb.texts):
    #         print(text)
    #         if mcb.has_extras():
    #             print("\t", mcb.extras[idx])