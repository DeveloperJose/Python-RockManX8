import io
from pathlib import Path
from typing import List

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

from core.io_util import FileStream

class OOPBlockMetadata:
    def __init__(self, reader: FileStream):
        self.width = reader.read_int()
        self.height = reader.read_int()

        self.unk1 = reader.read_int_array(4, 1)

        self.alt_w = reader.read_int()
        self.alt_h = reader.read_int()

        self.unk2 = reader.read_int_array(2)

        self.bpp = reader.read_int()
        self.bpp_dupe = reader.read_int()

        self.unk3 = reader.read_int_array(12, 1)
        print(f">> This image is {self.width} by {self.height} with bpp={self.bpp} | unk1={self.unk1} | alt_w={self.alt_w} | alt_h={self.alt_h} | unk2={self.unk2} | unk3={self.unk3}")

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
    def __init__(self, reader: FileStream, next_offset):
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
            raise Exception('Only textures allowed for now')
    
        # unk1 (12 bytes)
        self.unk1 = reader.read_int_array(12, 1)

        # id_str (16 bytes) - String of form ID_XX_###
        self.id_str = reader.read_string()

        # unk2 (4 bytes) - Seems to always be [0, 0]
        self.unk2 = reader.read_int_array(2)

        # Number of images in this block
        self.n_images = reader.read_int(4)
        print(f"> This block has {self.n_images} images with temp={self.temp_str} and id={self.id_str}")

        # unk3 (64 bytes)
        self.unk3 = reader.read_int_array(64, 1)

        # unk4 (20 bytes)
        self.unk4 = reader.read_int_array(20, 1)

        print(f"> block header={self.header} | magic1={self.magic1} | unk1={self.unk1} | unk2={self.unk2} | unk3={self.unk3} | unk4={self.unk4}")

        # Image metadata
        total_im_bytes = 0
        self.image_metadata = []
        for _ in range(self.n_images):
            metadata = OOPBlockMetadata(reader)
            self.image_metadata.append(metadata)
            total_im_bytes += (metadata.width * metadata.height) + 1024
        
        print(f"> All info ended at {reader.tell()}")

        # offd determines how much of the extra space in the next block header we will use
        offd = 12 if next_offset != reader.total_bytes() else 0
        next_offset += offd
        print(f"> We will use {offd} bytes in the next header")

        # Now let's find how many bytes we need to skip to end in the right place
        skip_bytes = next_offset - (reader.tell() + total_im_bytes)
        if skip_bytes < 0: # TODO: Fix bpp=8
            print(f"> Cannot skip!")
            return
        skip_data = reader.read(skip_bytes)
        print(f"> Skipped {skip_bytes} with offd {offd} | {np.count_nonzero(skip_data)} were interesting")

        # Raw image data
        self.image_rawdata = []
        for metadata in self.image_metadata:
            if metadata.bpp == 8:
                continue
            im_data = np.array([h for h in reader.read((metadata.width * metadata.height))], dtype=np.uint8)
            pal_data = np.array([h for h in reader.read(1024)], dtype=np.uint8)
            print(pal_data.dtype, pal_data)

            im = Image.frombytes('P', (metadata.width, metadata.height), im_data, 'raw', 'P', 0, -1)
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

            print([h for h in pal_data])
            
            # plt.subplot(1, 4, 3)
            # plt.imshow(im)
            # plt.axis('off')

            # for i in range(1024):
            # new_pal = np.roll(pal_data, i)
            new_pal = pal_data.copy()
            # print(new_pal[148*4:148*4+4])
            # new_pal[148*4:148*4+3] = [64, 57, 241]
            # new_pal[3::4] = 255
            arr1 = np.array(im.convert("L"), dtype=np.uint8)
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

            for i in [8, 40, 72, 104, 136, 168, 200, 232]:
                new_pal[i*4:(i+8)*4] = pal_data[(i+8)*4:(i+16)*4]

            for i in [16, 48, 80, 112, 144, 176, 208, 240]:
                new_pal[i*4:(i+8)*4] = pal_data[(i-8)*4:(i*4)]

            # im2 = np.array(Image.open("C:/Users/DevJ/Desktop/X.png").convert("RGBA"), dtype=np.uint8)
                
            im.putpalette(new_pal, 'RGBA')
            arr = np.array(im.convert('RGB'), dtype=np.uint8)

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
            
            plt.figure()
            plt.imshow(arr)
            plt.axis('off')
            plt.show()


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
        with open(path, 'rb') as file:
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

            self.unk2 = reader.read(self.offsets[0]-reader.tell())
            print(f'There are {self.offsets[0]-reader.tell()} bytes until the first offset, {np.count_nonzero(self.unk2)} of them are interesting')
            print(f"The offsets are {self.offsets}")

            self.blocks = []
            for block_idx, block_offset in enumerate(self.offsets):      
                reader.seek(block_offset)
                next_offset = reader.total_bytes() if block_idx == len(self.offsets)-1 else self.offsets[block_idx+1]
                self.blocks.append(OOPBlock(reader, next_offset))
                print(f"Block {block_idx} needs {next_offset-reader.tell()} bytes to reach the next offset {next_offset}\n\n")

    def save(self, spath: Path):
        with open(spath, 'wb') as file:
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

    opk_path = Path('C:/PROGRA~2/Steam/STEAMA~1/common/MEGAMA~1/nativeDX10/X8/romPC/data/opk/')
    arc_path = opk_path / 'title/2D_LOAD_SIGMA.arc'
    assert arc_path.exists()

    arctool_path = Path('../resources/ARCtool.exe')
    assert arctool_path.exists()

    output_fpath = opk_path/arc_path.parent.stem/arc_path.stem/'X8'/'data'/'opk'/arc_path.parent.stem/f'{arc_path.stem}.1E3EE6FB'

    # Extract arc if needed
    # original_path = Path('cockpit.1E3EE6FB')
    original_path = Path('logo.1E3EE6FB')

    # if not original_path.exists():
    #     assert output_fpath.exists()
    #     subprocess.call([str(arctool_path), '-x', '-pc', '-silent', str(arc_path)], creationflags=subprocess.CREATE_NO_WINDOW)
    #     output_fpath.rename(original_path)

    # im = Image.open("C:/Users/DevJ/Desktop/X.png").convert("RGBA").convert("P")
    # im.convert("L").save("X_2gray.png")
    # print([h for h in im.getpalette("RGBA")])
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
    # Open original OOP
    oop = OOPFile(original_path)

    # Play with OOP

    # Save OOP and compress to ARC
    # oop.save(output_fpath)
    # subprocess.call([str(arctool_path), '-c', '-pc', '-silent', str(opk_path / 'title/2D_LOAD_SIGMA')], creationflags=subprocess.CREATE_NO_WINDOW)
    
    # # Fix the ARC file so it doesn't crash the legacy collection
    # with open(arc_path, 'r+b') as file:
    #     file.seek(4)
    #     file.write(0x07.to_bytes(1, byteorder='little'))