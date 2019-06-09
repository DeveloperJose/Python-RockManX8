# -*- coding: utf-8 -*-
# Author: Jose G. Perez <josegperez@mail.com>
# Allows for the reading of MCB files for RockManX8
import io
import os
import numpy as np
from PIL import Image
import pylab as plt

LENGTH_HEADER = 16
LENGTH_SIZE = 2
LENGTH_TEXT_COUNT = 2
LENGTH_TEXT_OFFSET = 2
LENGTH_FILENAME = 16
LENGTH_FILENAME_EXTRA = 42



fileAbbr2 = ['NV', 'HB']
fileAbbr3 = ['SUB', 'OPT']
fileAbbr4 = ['DEMO', 'MENU', 'CHIP']
fileAbbr6 = ['RESULT']

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
        char_idx = 11

    if char_idx < 0 or char_idx >= len(char_icons):
        return 'Invalid Character: ' + str(char_idx)
    char_poses = poses[char_idx]

    # Pose 0 defaults to the first pose
    # Get pose string if possible
    if pose_idx < 0 or pose_idx >= len(char_poses):
        return 'OFB: ' + char_poses[0]
    return char_poses[pose_idx]

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
        return 'Unknown: ' + str(idx)
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
        conv = byte_to_str(int(byte, 16))
        if not conv:
            word += '_'
        else:
            word += conv

    return word

def byte_to_str(idx):
    if idx == 65533:
        return ' \n\t'
    elif idx < 0 or idx >= len(alphabet):
        return False
    else:
        return alphabet[idx]

def open_set(path):
    with open(path, 'rb') as file:
        print("======", path)
        header = file.read(104)

        enemies = set()
        while True:
            pos_before = file.tell()
            enemy = file.read(80)
            pos_after = file.tell()
            if pos_before == pos_after: # EOF
                break
            name = enemy[0:8].decode("utf-8", errors="replace")
            enemies.add(name)

        print("Enemies Present:")
        print(", ".join(enemies))

def open_mcb(path):
    with open(path, 'rb') as file:
        print("======", path)
        header = file.read(LENGTH_HEADER).decode("utf-8", errors="replace")
        size = int.from_bytes(file.read(LENGTH_SIZE), 'little')
        # print("Header", header)
        # print("Size", size, hex(size))

        text_count = int.from_bytes(file.read(LENGTH_TEXT_COUNT), 'little')
        # print("Text Count", text_count, hex(text_count))

        offsets = []
        offsets_h = []
        for i in range(text_count):
            offset = int.from_bytes(file.read(LENGTH_TEXT_OFFSET), 'little')
            offsets.append(offset)
            offsets_h.append(hex(offset))
        # print("Offsets", offsets, offsets_h)
        SEEK_OFFSET_END = file.tell()

        filename = file.read(LENGTH_FILENAME).decode("utf-8", errors='replace')
        files = []
        while is_file(filename):
            files.append(filename)
            filename = file.read(LENGTH_FILENAME).decode("utf-8", errors='replace')

        if len(files) > 0:
            # print("Found files", len(files), files)
            # Skip all the filenames and the first extra block
            offset_start = SEEK_OFFSET_END + (16 * len(files)) + 42
        else:
            offset_start = SEEK_OFFSET_END

        # print("Offset start", offset_start, hex(offset_start))
        # Extract the MCB information
        text_elements = []
        for i in range(text_count):
            # ******************** EXTRACT TEXT DATA
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

            # ******************** EXTRACT EXTRA DATA
            if len(files) == 0:
                print(repr(text), "\t{OFFSET}", str(hex(offset)))
            else:
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
                idx = [idx3, idx4, idx5, idx6, idx7, idx8, idx9, idx10, idx11, idx12, idx13, idx14, idx15]
                i = 0
                while i < len(idx):
                    current = idx[i]
                    if current <= 22:
                        break
                    i += 1

                if i >= len(idx):
                    idx_char = 255
                    idx_pose = 255
                else:
                    idx_char = idx[i]
                    idx_pose = idx[i + 1]

                print("%s [%s] : \n\t%s" %
                      (get_character(idx_char), get_pose(idx_char, idx_pose), text), # String Format
                      idx_char, idx_pose)

                # print(repr(text), "\t{OFFSET}", str(hex(offset)))
                if len(notFound) > 0:
                     print("\t\t", "Data Not In Alphabet: ", notFound)
                # print("\t\t", "[Sound Info]", "Voice:", get_voice(idx_voice), "BGM:", get_bgm(idx_bgm))
                # print("\t\t", "[Char Info]", get_character(idx_char), get_pose(idx_char, idx_pose), idx_char, idx_pose)
                # print("\t\t", "[Box Info]", get_textbox_pos(idx_text_pos), get_typing(idx_typing), get_arrow(idx_show_arrow))
                # print("Malformatted MCB")
                # print("\t\t\t "", {V=%s}{B=%s}{X1=%s}{?=%s}{X3=%s}{X4=%s}{X5=%s}{X6=%s}" %
                #       (hex(idx_voice), hex(idx_bgm), hex(idx1), hex(idx2), hex(idx3), hex(idx4), hex(idx5),
                #        hex(idx6)))
                # print("\t\t\t {X7=%s}{X8=%s}{X9=%s}{X10=%s}{X11=%s}{Char=%s}{CharPose=%s}" %
                #       (hex(idx7), hex(idx8), hex(idx9), hex(idx10), hex(idx11), hex(idx12), hex(idx13)))
                # print("\t\t\t {X14=%s}{X15=%s}{TextPos=%s}{X17=%s}{Typing=%s}{ShowArrow=%s}" %
                #       (hex(idx14), hex(idx15), hex(idx_text_pos), hex(idx17), hex(idx_typing),
                #        hex(idx_show_arrow)))
                #print("\t\t\t\t DATA:", data)

        return

# print("\n".join())
# open_mcb("mes/SPA/NV1_ST11.mcb")
# open_mcb("mes/SPA/NV1_ST11.mcb")

# for file in os.listdir("mes/USA/"):
#     open_mcb("mes/USA/" + file)

# open_mcb("mes/SPA/LABO_TXT.mcb")

#%% WPG
textures = []

with open('opk/title/spa/wpg/font_ID_FONT_000.wpg', 'rb') as file:
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
        im = np.array(im_raw_gray)[:240,:240]
        textures.append(im)

characters = []
for texture in textures:
    # Extract all 144 characters from the texture
    for row in range(12):
        for col in range(12):
            rstart = row * 20
            rend = rstart + 20
            cstart = col * 20
            cend = cstart + 20
            im_char = texture[rstart:rend, cstart:cend]
            characters.append(im_char)

# plt.figure()
# plt.imshow(im_raw_gray, cmap=plt.get_cmap('gray'))



# for texture in textures:
#     row_split = np.array(np.array_split(texture, 12))
#     for rs in row_split:
#         col_split = np.array_split(rs, 12)