import os
LENGTH_HEADER = 16
LENGTH_SIZE = 2
LENGTH_TEXT_COUNT = 2
LENGTH_TEXT_OFFSET = 2
LENGTH_FILENAME = 16
LENGTH_FILENAME_EXTRA = 42

alphabet = [' ', '!', '"', '%', '&', '(', ')', 'x', '+', '-', ',',
            '.', '/', ':', ';', '=', '?', '@', '[', ']', '_', '~', '`', '°', '..', '..'
            , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            , 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
            , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
            # 0x58
            , "'"]

# http://sprites-inc.co.uk/sprite.php?local=X/X8/Mugshots/
poses = [
    ['Normal R', 'Normal R', 'Surprised F', 'Angry R', 'Neutral Armor F'] , # X
    ['Normal Holding Sword F', 'Serious R', 'Eyes Closed R'], # Zero
    ['Smiling F', 'Serious R', 'Holding Gun R', 'Upset R'], # Axl
    ['Mic Hold L', 'Headphone Hold L', 'Worried F'], # Alia
    ['Headphone Hold L', 'Headphone Hold L', 'Blush F', 'Embarrassed F'], # Layer
    ['Headphone Hold L', 'Headphone Hold L', 'Mic Hold L', 'Thinking L', 'RD Lab F'], # Pallette
    ['Unknown'], # ??
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
    ['Real F', 'Copy L', 'Real F', 'Copy L'], # Sigma
    ['Regular F', 'Smirk F', 'Defeat F'], # Lumine
]
char_icons = ['X', 'Zero', 'Axl', 'BG Alia', 'BG Layer', 'BG Pallette', 'Probably Signas', 'Dr. Light', \
              'Optic Sunflower', 'Gravity Antonion' ,'Dark Mantis', 'Gigabolt Man-o-War', 'Burn Rooster', \
              'Avalanche Yeti' ,'Earthrock Trilobyte' ,'Bamboo Pandemonium' ,'Vile' , \
              'Sigma', 'Lumine']

fileAbbr2 = ['NV', 'HB']
fileAbbr3 = ['SUB', 'OPT']
fileAbbr4 = ['DEMO', 'MENU', 'CHIP']
fileAbbr6 = ['RESULT']

SHOW_EXTRA_DATA = True
SHOW_DATA = False
SHOW_TEXT = True

def get_voice(idx):
    return ""

def get_bgm(idx):
    return ""

def get_textbox_pos(idx):
    if idx == 1:
        return 'Down'
    return 'Up'

def get_typing(idx):
    return idx != 0

def get_arrow(idx):
    return idx == 1

def get_pose(char_idx, idx):
    # Navigator and Sigma FG/BG shenanigans
    if char_idx == 19:
        char_idx = 3
    elif char_idx == 20:
        char_idx = 4
    elif char_idx == 21:
        char_idx = 5
    elif char_idx == 22:
        char_idx = 11

    if char_idx < 0 or char_idx >= len(char_icons):
        return 'Invalid Character'
    char_poses = poses[char_idx]
    if idx < 0 or idx >= len(char_poses):
        return 'Probably ' + char_poses[0]
    return char_poses[idx]

def get_character(idx):
    if idx == 19:
        return 'FG Alia'
    elif idx == 20:
        return 'FG Layer'
    elif idx == 21:
        return 'FG Pallette'
    elif idx == 22:
        return 'Sigma'
    elif idx < 0 or idx >= len(char_icons):
        return 'Unknown'
    else:
        return char_icons[idx]

def to_hexpro(word):
    list = ""
    for i in range(len(word)):
        ch = word[i]
        try:
            idx = alphabet.index(ch)
            list += hex(idx)[2:] + " "
        except:
            list += "00 "

    return list


def is_file(str):
    return str[0:2] in fileAbbr2 or \
            str[0:3] in fileAbbr3 or \
            str[0:4] in fileAbbr4 or \
            str[0:6] in fileAbbr6

def hexpro_to_str(s):
    bytes = s.split()
    word = ""
    for byte in bytes:
        word += byte_to_str(int(byte, 16))

    return word

def byte_to_str(idx):
    if idx < 0 or idx >= len(alphabet):
        return False
    else:
        return alphabet[idx]

path = "mes/SPA/LABO_TIT.mcb"
def open_mcb(path):
    with open(path, 'rb') as file:
        header = file.read(LENGTH_HEADER).decode("utf-8", errors="replace")
        size = int.from_bytes(file.read(LENGTH_SIZE), 'little')
        print("Header", header)
        print("Size", size, hex(size))

        text_count = int.from_bytes(file.read(LENGTH_TEXT_COUNT), 'little')
        print("Text Count", text_count, hex(text_count))

        offsets = []
        offsets_h = []
        for i in range(text_count):
            offset = int.from_bytes(file.read(LENGTH_TEXT_OFFSET), 'little')
            offsets.append(offset)
            offsets_h.append(hex(offset))
        print("Offsets", offsets, offsets_h)
        SEEK_OFFSET_END = file.tell()

        filename = file.read(LENGTH_FILENAME).decode("utf-8", errors='replace')
        files = []
        while is_file(filename):
            files.append(filename)
            filename = file.read(LENGTH_FILENAME).decode("utf-8", errors='replace')

        if len(files) > 0:
            print("Found files", len(files), files)
            # Skip all the filenames and the first extra block
            offset_start = SEEK_OFFSET_END + (16 * len(files)) + 42
        else:
            offset_start = SEEK_OFFSET_END

        print("Offset start", offset_start, hex(offset_start))
        # Extract the MCB information
        text_elements = []
        for i in range(text_count):
            offset = offset_start + offsets[i]
            file.seek(offset)

            text = ""
            data = ""
            notFound = ""
            data_int = int.from_bytes(file.read(2), 'little')
            while data_int != 65535: # 65535 = 0XFFFF
                data_str = byte_to_str(data_int)
                if not data_str:
                    notFound += hex(data_int) + ","
                    text += "_"
                else:
                    text += data_str
                data += str(hex(data_int)) + ","

                data_int = int.from_bytes(file.read(2), 'little')

            if SHOW_EXTRA_DATA:
                if len(files) > 0:
                    file.seek(offset - LENGTH_FILENAME_EXTRA)
                    idx_voice = int.from_bytes(file.read(2), 'little')
                    idx_bgm = int.from_bytes(file.read(2), 'little')
                    idx1 = int.from_bytes(file.read(2), 'little')
                    idx2 = int.from_bytes(file.read(2), 'little')
                    idx3 = int.from_bytes(file.read(2), 'little')
                    idx4 = int.from_bytes(file.read(2), 'little')
                    idx5 = int.from_bytes(file.read(2), 'little')
                    idx6 = int.from_bytes(file.read(2), 'little')
                    idx7 = int.from_bytes(file.read(2), 'little')
                    idx8 = int.from_bytes(file.read(2), 'little')
                    idx9 = int.from_bytes(file.read(2), 'little')
                    idx10 = int.from_bytes(file.read(2), 'little')
                    idx11 = int.from_bytes(file.read(2), 'little')
                    idx12 = int.from_bytes(file.read(2), 'little')
                    idx13 = int.from_bytes(file.read(2), 'little')
                    idx14 = int.from_bytes(file.read(2), 'little')
                    idx15 = int.from_bytes(file.read(2), 'little')
                    idx_text_pos = int.from_bytes(file.read(2), 'little')
                    idx17 = int.from_bytes(file.read(2), 'little')
                    idx_typing = int.from_bytes(file.read(2), 'little')
                    idx_show_arrow = int.from_bytes(file.read(2), 'little')

                    # Find char and pose
                    idx = [idx4, idx5, idx6, idx7, idx8, idx9, idx10, idx11, idx12, idx13, idx14, idx15]
                    i = 0
                    while i < len(idx):
                        current = idx[i]
                        if current <= 22:
                            break
                        i += 1

                    idx_char = idx[i]
                    idx_pose = idx[i + 1]

                    frmt = "%s\t[%s]\n\t%s" % (get_character(idx_char), get_pose(idx_char, idx_pose), repr(text))
                    print(frmt)

                    # print(repr(text), "\t{OFFSET}", str(hex(offset)))
                    # if len(notFound) > 0:
                    #     print("\t\t", "Data Not In Alphabet: ", notFound)
                    # print("\t\t", "[Sound Info]", "Voice:", get_voice(idx_voice), "BGM:", get_bgm(idx_bgm))
                    # print("\t\t", "[Char Info]", get_character(idx_char), get_pose(idx_char, idx_pose), idx_char, idx_pose)
                    # print("\t\t", "[Box Info]", get_textbox_pos(idx_text_pos), get_typing(idx_typing), get_arrow(idx_show_arrow))
                    # print("\t\t\t "", {V=%s}{B=%s}{X1=%s}{?=%s}{X3=%s}{X4=%s}{X5=%s}{X6=%s}" %
                    #       (hex(idx_voice), hex(idx_bgm), hex(idx1), hex(idx2), hex(idx3), hex(idx4), hex(idx5), hex(idx6)))
                    # print("\t\t\t {X7=%s}{X8=%s}{X9=%s}{X10=%s}{X11=%s}{Char=%s}{CharPose=%s}" %
                    #       (hex(idx7), hex(idx8), hex(idx9), hex(idx10), hex(idx11), hex(idx12), hex(idx13)))
                    # print("\t\t\t {X14=%s}{X15=%s}{TextPos=%s}{X17=%s}{Typing=%s}{ShowArrow=%s}" %
                    #       (hex(idx14), hex(idx15), hex(idx_text_pos), hex(idx17), hex(idx_typing), hex(idx_show_arrow)))

            elif SHOW_TEXT:
                print(repr(text), "\t{OFFSET}", str(hex(offset)))

            if SHOW_DATA:
                print("\t\t\t\t DATA:", data)

        return

# print("\n".join())
# open_mcb("mes/SPA/NV1_ST11.mcb")
# open_mcb("mes/SPA/NV1_ST11.mcb")
#
# for file in os.listdir("mes/SPA/"):
#     open_mcb("mes/SPA/" + file)

open_mcb("mes/SPA/LABO_TXT.mcb")