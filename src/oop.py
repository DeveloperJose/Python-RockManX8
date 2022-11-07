import io
import pathlib
import subprocess
import multiprocess
import copy

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFile
from tqdm import tqdm

from core.io_util import FileStream
from core.wpg import WPGFile

if __name__ == "__main__":
    op_file = pathlib.Path('textures/2D_LOAD_ELEVATOR.1E3EE6FB')

    file = open(op_file, 'rb')
    reader1 = FileStream(file)
    all_bytes = reader1.read_remaining_bytes()
    file.close()
    
    reader = FileStream(io.BytesIO(all_bytes))

    oop_header = reader.read_string(8)
    file_size = reader.read_int(4)
    unk1 = reader.read_byte_array(4)
    count = reader.read_int(4)
    print("There are", count, "files")

    offsets = []

    for _ in range(count):
        offset = reader.read_int(4)
        offsets.append(offset)
        print(f"offset = {offset:X}")

    file_size_dupe = reader.read_int(4)

    all_shapes = {off: [] for off in offsets}
    all_n_images = {off: -1 for off in offsets}


    def process(i, i2):
        with open('textures/2D_LOAD_ELEVATOR.1E3EE6FB', 'rb') as file:
            reader = FileStream(file)
            reader.seek(i)
            arr = reader.read_int_array(768, size_bytes=1)

            im = Image.open('original.png')
            if max(arr) != 0:
                im.putpalette(arr, 'RGB')
                im.save(f'figures/{i}_rgb.png')

            reader.seek(i)
            arr = reader.read_int_array(1024, size_bytes=1)
            if max(arr) != 0:
                im.putpalette(arr, 'RGBA')
                im.save(f'figures/{i}_rgba.png')

    for file_idx, offset in enumerate(offsets):
        all_extra_ints = {}
        reader.seek(offset)
        wpg_header = reader.read_byte_array(16)
        wpg_temp = reader.read_string()

        wpg_magic1 = reader.read_byte_array(20)

        wpg_id = reader.read_string()

        wpg_magic2 = reader.read_byte_array(4)

        wpg_n_images = reader.read_int(4)
        all_n_images[offset] = wpg_n_images

        wpg_unk1 = reader.read_byte_array(84)
        
        for i in range(wpg_n_images):
            width = reader.read_int()
            height = reader.read_int()

            all_shapes[offset].append((width, height))
            wpg_unk2 = reader.read_int_array(14)
            all_extra_ints[i] = wpg_unk2
            # wpg_unk2 = reader.read_byte_array(28)
            print(offset, i, width, height, wpg_unk2)

        data_start_offset = reader.tell()
        print('Data starting at', data_start_offset)
        for i in range(wpg_n_images):
            shape = all_shapes[offset][i]
            want = shape[0]*shape[1]

            # elevator 1024 0 512 448 [256, 0, 0, 0, 2, 0, 16, 16, 33024, 3, 0, 0, 0, 0]
            bpp_mode = all_extra_ints[i][6]
            print(f'Currently idx={i}, tell={reader.tell()}/{reader.total_bytes()}, want={want}, bpp={bpp_mode}')
            if bpp_mode == 8:
                s1 = min(all_extra_ints[i][0], shape[0])
                s2 = min(all_extra_ints[i][8], shape[1])
                shape = (s1, s2)
            im_data = reader.read(shape[0]*shape[1])
            if not im_data:
                print(f'Ran out of bytes')
                break
            
            IM = Image.frombytes("P", shape, im_data, 'raw', 'P', 0, -1)
            IM.save('original.png')

            # images = [copy.deepcopy(IM) for _ in range(reader.total_bytes())]
            idxs = list(range(reader.total_bytes()))
            pbar = tqdm(total=len(idxs))

            with multiprocess.Pool(5) as pool:
                for _ in pool.starmap(process, enumerate(idxs)):
                    pbar.update(1)