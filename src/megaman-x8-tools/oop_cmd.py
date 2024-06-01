import io
import math
from pathlib import Path
from typing import List

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

from core.io_util import FileStream

D = {}


class OOPBlockMetadata:
    def __init__(self, reader: FileStream):
        self.width = reader.read_int()
        self.height = reader.read_int()

        self.alt_w1 = reader.read_int()
        self.alt_h1 = reader.read_int()

        self.alt_w2 = reader.read_int()
        self.alt_h2 = reader.read_int()

        self.unk2 = reader.read_int_array(2)

        self.bpp = reader.read_int()
        self.bpp_dupe = reader.read_int()

        self.unk3 = reader.read_int_array(12, 1)
        print(
            f">> This image is {self.width} by {self.height} with bpp={self.bpp} | alt_w1={self.alt_w1} | alt_h1={self.alt_h1} | alt_w2={self.alt_w2} | alt_h2={self.alt_h2} | unk2={self.unk2} | unk3={self.unk3}"
        )

        # self.w = min(self.width, self.alt_w1) if self.alt_w1 != 0 else self.width
        # self.h = min(self.height, self.alt_h1) if self.alt_h1 != 0 else self.height
        # print(">>", self.w, self.h)
        self.w = self.width // 2
        self.h = self.height

    def im_size_bytes(self):
        if self.bpp == 16:
            return (self.width * self.height) + 1024
        elif self.bpp == 8:
            return (self.w * self.h) + 256
        else:
            raise Exception("Invalid bpp", self.bpp)

    def write(self, writer: FileStream):
        writer.write_int(self.width)
        writer.write_int(self.height)
        writer.write_int_array(self.unk1, 1)
        writer.write_int(self.alt_w)
        writer.write_int(self.alt_h)
        writer.write_int_array(self.unk2, 1)
        writer.write_int(self.bpp)
        writer.write_int(self.bpp_dupe)
        writer.write_int_array(self.unk3, 1)


class OOPBlock:
    def __init__(self, reader: FileStream, next_offset, block_idx, filename):
        # header (16 bytes)
        # 12 bytes - Extra space for previous image palette
        # 4 bytes - ???
        self.header = reader.read_int_array(16, 1)

        # temp_str (16 bytes)
        # 16 bytes - String in format "temp#"
        self.temp_str = reader.read_string()

        # magic1 (6 bytes)
        # 4 bytes - Unknown
        # 1 byte - Resource Type
        # 1 byte - Always 0
        self.magic1 = reader.read_int_array(4)

        wpg_type = self.magic1[2]
        if wpg_type != 4:
            print(
                f"Cannot parse OPK type",
                wpg_type,
                "at",
                reader.tell(),
                self.header,
                self.temp_str,
                self.magic1,
            )
            val = (reader.tell(), f"s={next_offset-reader.tell()}")
            if wpg_type in D:
                D[wpg_type].append(val)
            else:
                D[wpg_type] = [val]
            return

        # unk1 (12 bytes)
        self.unk1 = reader.read_int_array(12, 1)

        # id_str (16 bytes) - String of form ID_XX_###
        self.id_str = reader.read_string()

        # unk2 (4 bytes) - Seems to always be [0, 0]
        self.unk2 = reader.read_int_array(2)

        # Number of images in this block
        self.n_images = reader.read_int(4)
        print(
            f"> This block{block_idx} has {self.n_images} images with temp={self.temp_str} and id={self.id_str} | {wpg_type}"
        )
        if self.n_images == 0:
            print(f"Has 0 images")
            return

        # unk3 (64 bytes)
        self.unk3 = reader.read_int_array(64, 1)

        # unk4 (20 bytes)
        self.unk4 = reader.read_int_array(20, 1)

        print(
            f"> block header={self.header} | magic1={self.magic1} | unk1={self.unk1} | unk2={self.unk2} | unk3={self.unk3} | unk4={self.unk4}"
        )

        # Image metadata
        total_im_bytes = 0
        self.image_metadata = []
        for _ in range(self.n_images):
            metadata = OOPBlockMetadata(reader)
            self.image_metadata.append(metadata)
            total_im_bytes += metadata.im_size_bytes()

            if metadata.width == 0 and metadata.height == 0:
                print("> 0 width and height")
                return

        print(f"> All info ended at {reader.tell()}")

        # offd determines how much of the extra space in the next block header we will use
        offd = 12 if next_offset != reader.total_bytes() else 0
        next_offset += offd
        print(f"> We will use {offd} bytes in the next header")

        # Now let's find how many bytes we need to skip to end in the right place
        skip_bytes = next_offset - (reader.tell() + total_im_bytes)
        if skip_bytes < 0:
            print(f"> Cannot skip!", skip_bytes)
            return
        skip_data = reader.read(skip_bytes)

        print(
            f"> Skipped {skip_bytes} with offd {offd} ended at {reader.tell()}/{reader.total_bytes()} | {np.count_nonzero(skip_data)} were interesting"
        )
        # Raw image data
        self.image_rawdata = []
        for idx, metadata in enumerate(self.image_metadata):
            print(f"Begin at {reader.tell()}/{reader.total_bytes()} ")
            if metadata.bpp == 8:
                im_data = np.array(
                    [h for h in reader.read((metadata.w * metadata.h))], dtype=np.uint8
                )
                pal_data = np.array([h for h in reader.read(256)], dtype=np.uint8)
                print("w by h", metadata.w, metadata.h)
                im = Image.frombytes(
                    "P", (metadata.w, metadata.h), im_data, "raw", "P", 0, -1
                )

                # im2 = Image.open("C:/Users/DevJ/Desktop/mission_complete.png").convert("RGBA")
                # im2_p = im2.convert('RGB').quantize(255)

                new_pal = pal_data.copy()
                for i in [
                    0,
                    8,
                    13,
                    44,
                    61,
                    85,
                    86,
                    87,
                    88,
                    89,
                    90,
                    91,
                    92,
                    94,
                    95,
                    97,
                    98,
                    99,
                    100,
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                    120,
                    121,
                    122,
                    123,
                    124,
                    125,
                    126,
                    127,
                    130,
                    131,
                    132,
                    133,
                    134,
                    135,
                    136,
                    137,
                    138,
                    139,
                    140,
                    141,
                    143,
                    144,
                    146,
                    147,
                    148,
                    149,
                    150,
                    151,
                    152,
                    153,
                    154,
                    155,
                    156,
                    157,
                    158,
                    159,
                    160,
                    161,
                    162,
                    163,
                    164,
                    166,
                    167,
                    168,
                    169,
                    170,
                    171,
                    172,
                    173,
                    174,
                    175,
                    178,
                    179,
                    180,
                    181,
                    182,
                    183,
                    184,
                    185,
                    186,
                    187,
                    188,
                    189,
                    190,
                    191,
                    194,
                    195,
                    196,
                    197,
                    198,
                    199,
                    200,
                    201,
                    202,
                    203,
                    204,
                    205,
                    206,
                    207,
                    210,
                    211,
                    212,
                    214,
                    215,
                    216,
                    217,
                    218,
                    219,
                    220,
                    221,
                    222,
                    223,
                    224,
                    226,
                    227,
                    228,
                    229,
                    231,
                    233,
                    234,
                    235,
                    236,
                    237,
                    238,
                    239,
                    240,
                    242,
                    243,
                    244,
                    245,
                    246,
                    247,
                    248,
                    249,
                    250,
                    251,
                    252,
                    253,
                ]:
                    # for i in [8//3, 40//3, 72//3, 104//3, 136//3, 168//3, 200//3, 232//3, 16//3, 48//3, 80//3, 112//3, 144//3, 176//3, 208//3, 240//3]:
                    i = i // 3
                    start = i * 3
                    block = math.floor(start / 16)
                    bstart = block * 4
                    # print(i, block, start, len(new_pal), new_pal[start:start+3], pal_data[bstart:bstart+3])
                    new_pal[start : start + 3] = pal_data[bstart : bstart + 3]
                im.putpalette(new_pal)
                im.convert("RGB").save(
                    f"figures3/{filename}_b{block_idx}_{self.id_str}_im{idx}_bpp8.png"
                )
                # print([h for h in new_pal])

                # def find(al):
                #     for i in range(len(new_pal)-3):
                #         if np.array_equal(new_pal[i:i+3], al):
                #             print(i)

                # plt.subplot(2, 2, 1)
                # plt.imshow(im, cmap='gray')

                # plt.subplot(2, 2, 2)
                # im.putpalette(new_pal)
                # plt.imshow(im)

                # plt.subplot(2, 2, 3)
                # plt.imshow(im2_p.convert('L'), cmap='gray')

                # plt.subplot(2, 2, 4)
                # plt.imshow(im2_p)

                # plt.show(block=False)

                # import pdb
                # pdb.set_trace()

                # print([h for h in new_pal], '\n')
                # print(im2_p.getpalette())
                # for i in list(range(17)):
                #     s1 = i*3
                #     s2 = 60-(i*4)
                #     if i == 6:
                #         s2 -= 4
                #     elif i == 7 or i == 10 or i == 11:
                #         s2 += 4
                #     elif i == 9:
                #         s2 -= 8

                #     print(i, '=>', s2, pal_data[s2:s2+3])
                #     new_pal[s1:s1+3] = pal_data[s2:s2+3]

                # for i in range(17, 32):
                #     s1 = i*3
                #     s2 = 60 + (i//17 * 4)
                #     new_pal[s1:s1+3] = pal_data[s2:s2+3]

                # arr1 = np.array(new_pal)
                # arr2 = np.array(im2_p.getpalette())

                # D = {}
                # for i in range(len(pal_data)-3):
                #     key = (pal_data[i], pal_data[i+1], pal_data[i+2])
                #     if key in D:
                #         D[key].add(i)
                #     else:
                #         D[key] = set([i])

                # tr = 0
                # for i in range(85-3):
                #     a1 = arr1[i*3:i*3+3]
                #     a2 = arr2[i*3:i*3+3]
                #     # if not np.array_equal(a2, a2):
                #     if not np.array_equal(a1, a2):
                #         print(i, a1, '==', a2, np.array_equal(a1, a2), 60-(i*4), D[(a2[0], a2[1], a2[2])])
                #     tr += 1 if np.array_equal(a1, a2) else 0
                # print(tr, '/', 85-3)

                # print(np.array(im2_p.getpalette('RGB')[0:256]))

                # im.putpalette(im2_p.getpalette('RGB')[0:256])
                # plt.imshow(im2_p)
                # plt.show()
                # print(pal_data)
                # for idx, n in enumerate(pal_data):
                #     if idx+2 >= len(pal_data):
                #         break
                #     l = [n, pal_data[idx+1], pal_data[idx+2]]
                #     if l == [255, 255, 251]:
                #         print('0', idx)
                #     elif l == [255, 254, 175]:
                #         print('1', idx)
                #     elif l == [250, 253, 121]:
                #         print('2', idx)
                #     elif l == [98, 225, 1]:
                #         print('6', idx, 60-(6*4))
                #     elif l == [174, 207, 4]:
                #         print('7', idx, 60-(7*4))
                #     elif l == [157, 191, 4]:
                #         print('8', idx, 60-(8*4))
                #     elif l == [124, 133, 19]:
                #         print('9', idx, 60-(9*4))
                #     elif l == [116, 186, 5]:
                #         print('10', idx, 60-(10*4))

                # new_pal = pal_data.copy()

                # # for i in [8]:
                # #     new_pal[i*4:(i+8)*4] = pal_data[(i+8)*4:(i+16)*4]

                # print3(new_pal, im2_p.getpalette())
                # plt.figure()
                # plt.imshow(im2_p)
                # plt.show()

                # arr = np.array(im.convert('RGB'))
                # im.putpalette(new_pal, 'RGB')
                # D = {h:set() for h in range(256)}
                # for r in range(arr.shape[0]):
                #     for c in range(arr.shape[1]):
                #         v1 = arr[r, c, [0, 1, 2]]
                #         v2 = im2[r, c, [0, 1, 2]]

                #         gray = arr1[r, c]
                #         dist = np.linalg.norm(v2 - v1)
                #         D[gray].add(dist)
                # for i in range(0, 255, 8):
                #     print(i, [D[h+i] for h in range(7)])
            else:
                if metadata.width == 0 or metadata.height == 0:
                    print("Skipping w=0 or h=0")
                    continue
                im_data = np.array(
                    [h for h in reader.read((metadata.width * metadata.height))],
                    dtype=np.uint8,
                )
                pal_data = np.array([h for h in reader.read(1024)], dtype=np.uint8)
                im = Image.frombytes(
                    "P", (metadata.width, metadata.height), im_data, "raw", "P", 0, -1
                )
                new_pal = pal_data.copy()
                for i in [8, 40, 72, 104, 136, 168, 200, 232]:
                    new_pal[i * 4 : (i + 8) * 4] = pal_data[(i + 8) * 4 : (i + 16) * 4]

                for i in [16, 48, 80, 112, 144, 176, 208, 240]:
                    new_pal[i * 4 : (i + 8) * 4] = pal_data[(i - 8) * 4 : (i * 4)]

                im.putpalette(new_pal, "RGBA")
                im.convert("RGB").save(
                    f"figures3/{filename}_b{block_idx}_{self.id_str}_im{idx}.png"
                )

            # plt.figure()
            # plt.imshow(im)
            # plt.suptitle(f'block{block_idx} im{idx} bpp{metadata.bpp}')
            # plt.axis('off')
            # plt.show()
            print(f"End at {reader.tell()}/{reader.total_bytes()} ")
            # im.putpalette(pal_data, 'RGBA')

            # alpha_min = arr[:, :, 3].min()
            # alpha_max = arr[:, :, 3].max()
            # arr = arr.astype(np.int32)
            # print(arr.dtype, arr.shape, alpha_min, alpha_max, arr[:, :, 3].mean())
            # if alpha_min == alpha_max == 128:
            #     print("> Overwriting alpha")

            # fig, curr = plt.subplots(figsize=(10, 10))
            # curr.set_xticklabels([])
            # curr.set_yticklabels([])
            # curr.imshow(im)
            # curr.set_title(f"ID={self.id_str}")
            # plt.show()

            # print([h for h in pal_data])

            # plt.subplot(1, 4, 3)
            # plt.imshow(im)
            # plt.axis('off')

            # for i in range(1024):
            # new_pal = np.roll(pal_data, i)

            # print(new_pal[148*4:148*4+4])
            # new_pal[148*4:148*4+3] = [64, 57, 241]
            # new_pal[3::4] = 255
            # arr1 = np.array(im.convert("L"), dtype=np.uint8)
            # for r in range(arr1.shape[0]):
            #     for c in range(arr1.shape[1]):
            #         p = arr1[r, c]
            #         if p == 152 or p == 144 or p == 140 or p == 164
            # for i in range(1024):
            #     if np.array_equal(new_pal[i:i+3], np.array([92, 128, 143])):
            #         print("144=> found1 at ", i//4)
            #     elif np.array_equal(new_pal[i:i+3], np.array([80, 145, 170])):
            #         print("128|131|(156)|166|162|173|181|184|190|=> found2 at", i//4)
            #     elif np.array_equal(new_pal[i:i+3], np.array([129, 213, 238])):
            #         print("(214)|208|202=|233> found2 at", i//4)

            # im2 = np.array(Image.open("C:/Users/DevJ/Desktop/X.png").convert("RGBA"), dtype=np.uint8)

            # arr = np.array(im.convert('RGB'), dtype=np.uint8)

            # D = {h:set() for h in range(256)}
            # for r in range(arr.shape[0]):
            #     for c in range(arr.shape[1]):
            #         v1 = arr[r, c, [0, 1, 2]]
            #         v2 = im2[r, c, [0, 1, 2]]
            #     # if gray == 156 or gray == 143 or gray == 214 or gray==128 or gray==162:
            #         gray = arr1[r, c]
            #         dist = np.linalg.norm(v2 - v1)
            #         D[gray].add(dist)

            # # print(D)
            # for i in range(0, 255, 8):
            #     print(i, [D[h+i] for h in range(7)])
            # im.convert('RGBA').save(f'figures4/{i}.png')
            # arr[:, :, 3] = 255
            # plt.subplot(1, 4, 4)

    def write(self, writer: FileStream):
        writer.write_int_array(self.header, 1)
        writer.write_string(self.temp_str)
        writer.write_int_array(self.magic1, 1)
        writer.write_int_array(self.unk1, 1)
        writer.write_string(self.id_str)
        writer.write_int_array(self.unk2, 1)
        writer.write_int(self.n_images)
        writer.write_int_array(self.unk3, 1)
        writer.write_int_array(self.unk4, 1)

        for metadata in self.image_metadata:
            metadata.write(writer)

        for rawdata in self.image_rawdata:
            writer.write(rawdata)


class OOPFile:
    def __init__(self, path: Path):
        self.path = path

        # if self.path is not None and self.path.exists():
        self.__load_from__file(path)

    def __load_from__file(self, path: Path):
        with open(path, "rb") as file:
            reader = FileStream(file)

            self.header = reader.read_string(8)
            self.file_size = reader.read_int(4)
            self.unk1 = reader.read_int_array(2)

            self.n_files = reader.read_int(4)
            self.offsets = []

            for _ in range(self.n_files):
                offset = reader.read_int(4)
                self.offsets.append(offset)

            self.file_size_dupe = reader.read_int(4)

            self.unk2 = reader.read(self.offsets[0] - reader.tell())
            print(
                f"There are {self.offsets[0]-reader.tell()} bytes until the first offset, {np.count_nonzero(self.unk2)} of them are interesting"
            )
            print(f"The offsets are {self.offsets}")

            self.blocks = []
            for block_idx, block_offset in enumerate(self.offsets):
                reader.seek(block_offset)
                next_offset = (
                    reader.total_bytes()
                    if block_idx == len(self.offsets) - 1
                    else self.offsets[block_idx + 1]
                )
                self.blocks.append(OOPBlock(reader, next_offset, block_idx, path.stem))
                print(
                    f"Block {block_idx} needs {next_offset-reader.tell()} bytes to reach the next offset {next_offset}\n\n"
                )

    def save(self, spath: Path):
        with open(spath, "wb") as file:
            writer = FileStream(file)
            writer.write_string(self.header, 8)
            writer.write_int(self.file_size, 4)
            writer.write_int_array(self.unk1)
            writer.write_int(self.n_files)
            for offset in self.offsets:
                writer.write_int(offset, 4)
            writer.write_int(self.file_size_dupe, 4)

            for block in self.blocks:
                block: OOPBlock
                block.write(writer)


if __name__ == "__main__":
    import subprocess
    from tqdm import tqdm

    opk_path = Path(
        "C:/PROGRA~2/Steam/STEAMA~1/common/MEGAMA~1/nativeDX10/X8/romPC/data/opk/"
    )
    arc_path = opk_path / "title/2D_LOAD_SIGMA.arc"
    assert arc_path.exists()

    arctool_path = Path("../resources/ARCtool.exe")
    assert arctool_path.exists()

    output_fpath = (
        opk_path
        / arc_path.parent.stem
        / arc_path.stem
        / "X8"
        / "data"
        / "opk"
        / arc_path.parent.stem
        / f"{arc_path.stem}.1E3EE6FB"
    )

    # Extract arc if needed
    # original_path = Path('cockpit.1E3EE6FB')
    original_path = Path("logo.1E3EE6FB")

    # if not original_path.exists():
    #     assert output_fpath.exists()
    #     subprocess.call([str(arctool_path), '-x', '-pc', '-silent', str(arc_path)], creationflags=subprocess.CREATE_NO_WINDOW)
    #     output_fpath.rename(original_path)

    # im = Image.open("C:/Users/DevJ/Desktop/mission_complete.png").convert("RGBA").convert("P")
    # im.convert("L").save("X_2gray.png")
    # print([h for h in im.getpalette("RGB")])
    # pal = [h for h in im.getpalette("RGBA")]
    # for i in range(len(pal)-1, 0, -1):
    #     if pal[i] != 0:
    #         break
    # print(pal[i+1], i+1)
    # plt.subplot(1, 4, 1)
    # plt.imshow(im.convert("L"), cmap='gray')
    # plt.axis('off')

    # plt.subplot(1, 4, 2)
    # plt.imshow(im)
    # plt.axis('off')
    # plt.figure()
    # plt.imshow(im)
    # plt.show()

    storage_path = Path("textures")
    # failed = []
    # for fpath in tqdm(list(storage_path.glob('*.1E3EE6FB'))):
    #     try:
    #         OOPFile(fpath)
    #     except Exception as ex:
    #         print("Failed with", str(ex))
    #         failed.append(fpath)

    # print('Failed', failed)

    # Open original OOP
    oop = OOPFile(storage_path / "PL_X.1E3EE6FB")
    print(D)

    # Play with OOP

    # Save OOP and compress to ARC
    # oop.save(output_fpath)
    # subprocess.call([str(arctool_path), '-c', '-pc', '-silent', str(opk_path / 'title/2D_LOAD_SIGMA')], creationflags=subprocess.CREATE_NO_WINDOW)

    # # Fix the ARC file so it doesn't crash the legacy collection
    # with open(arc_path, 'r+b') as file:
    #     file.seek(4)
    #     file.write(0x07.to_bytes(1, byteorder='little'))
