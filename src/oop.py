import io
import pathlib
import subprocess
import joblib

import matplotlib.pyplot as plt
import multiprocess
import numpy as np
from core.io_util import FileStream
from core.wpg import WPGFile
from PIL import Image, ImageFile
from tqdm import tqdm

def int_list_to_hex(l):
    return [f'{h:X}' for h in l]

SHOW_FIGURES = False
DEBUG = False

figures_dir = pathlib.Path('figures2')
if not figures_dir.exists():
    figures_dir.mkdir()

all_remains = []
failed_files = []
ran_out_of_bytes = []
exceptions = set()

ALL_TYPES = set()

D1 = 1024

log_path = pathlib.Path('figures2/log.txt')
log_file = open(log_path, 'w')
def printd(st):
    log_file.write(st + '\n')

if DEBUG:
    l = []

    # if not DEBUG_ONE:
    # l += [pathlib.Path('/home/jperez/data/textures/2D_LOAD_ATARI00.1E3EE6FB')]
    # l += [pathlib.Path('/home/jperez/data/textures/2D_LOAD_ELEVATOR - Copy.1E3EE6FB')]
    # l += [pathlib.Path('/home/jperez/data/textures/2D_LOAD_SIGMA.1E3EE6FB')]
    l += [pathlib.Path('/home/jperez/data/textures/cockpit.1E3EE6FB')]
else:
    l = tqdm(list(pathlib.Path('/home/jperez/data/textures').glob('*.1E3EE6FB')))

for op_file in l:
    try:
        file = open(op_file, 'rb')
    except PermissionError:
        file.close()
        printd('Cannot open due to permission')
        continue
    
    try:
        reader = FileStream(file)

        oop_header = reader.read_string(8)
        file_size = reader.read_int(4)
        unk1 = reader.read_int_array(2)

        count = reader.read_int(4)
        printd(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        printd(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        printd(f'{count} files in {op_file.name} | unk1={unk1}')

        offsets = []
        for _ in range(count):
            offset = reader.read_int(4)
            offsets.append(offset)

        file_size_dupe = reader.read_int(4)

        all_n_images = {}

        # There are 12 zeros in the first offset so offd=0
        all_wpg_offd = [0]

        for file_idx, offset in enumerate(offsets):
            reader.seek(offset)

            all_extra_ints = {}
            all_shapes = {}
            all_bpps = {}
            all_alt_w = {}
            all_alt_h = {}
            all_wpg_unk3 = {}
            
            # wpg_header (16 bytes)
            # 12 bytes - Extra space for previous image palette
            # 4 bytes - Always [108, 0, 1, 1]
            wpg_header = reader.read_int_array(16, 1)
            assert wpg_header[-4:] == [108, 0, 1, 1]

            # wpg_temp (16 bytes)
            # 16 bytes - String in format "temp#"
            wpg_temp = reader.read_string()

            # wpg_magic1_p1 (20 bytes)
            # 4 bytes - Unknown
            # 1 byte - Resource Type
            # 1 byte - Always 0
            wpg_magic1_p1 = reader.read_int_array(4)
            # assert wpg_magic1_p1[:2] == [0, 0], str(wpg_magic1_p1)
            assert wpg_magic1_p1[3] == 0

            wpg_type = wpg_magic1_p1[2]
            ALL_TYPES.add(wpg_type)

            # Only parse 2D textures for now
            if wpg_type != 4:
                continue

            # 12 bytes - Unknown
            wpg_magic1_p2 = reader.read_int_array(12, 1)

            # 16 bytes - String of form ID_XX_###
            wpg_id = reader.read_string()

            # 4 bytes - Always [0, 0]
            wpg_magic2 = reader.read_int_array(2)
            assert wpg_magic2 == [0, 0]

            wpg_n_images = reader.read_int(4)
            all_n_images[offset] = wpg_n_images
            printd(f'[File{file_idx+1}/{len(offsets)}] at {offset}=0x{offset:X} with {wpg_n_images} images')
            printd(f'Header={wpg_header}')
            printd(f'Header(hex)={int_list_to_hex(wpg_header)}')
            printd(f'type={wpg_type}, magic1_p1={wpg_magic1_p1}')
            printd(f'magic1_p2={wpg_magic1_p2}')
            printd(f'Temp={wpg_temp}, ID={wpg_id}, Magic2={wpg_magic2}')

            wpg_unk1_p1 = reader.read_int_array(64, 1)
            # assert wpg_unk1_p1 == [255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], str(wpg_unk1_p1)

            wpg_unk1_p2 = reader.read_int_array(20, 1)
            reader.seek(reader.tell()-20)
            wpg_unk1_p2_b2 = reader.read_int_array(10)

            printd(f'\tunk1_p2={wpg_unk1_p2}')
            printd(f'\tunk1_p2(hex)={int_list_to_hex(wpg_unk1_p2)}')
            printd(f'\tunk1_p2_b2{wpg_unk1_p2_b2}')
            printd(f'\tunk1_p2_b2(hex)={int_list_to_hex(wpg_unk1_p2_b2)}')

            printd(f'WPG HEADER ENDS AT {reader.tell()}')

            filler = 0
            for i in range(wpg_n_images):
                printd(f'\t[im{i+1}/{wpg_n_images}]')
                width = reader.read_int()
                height = reader.read_int()
                printd(f'\t[shape] {width}x{height}')

                deb = reader.read_int_array(4, 1)
                reader.seek(reader.tell()-4)
                deb_b2 = reader.read_int_array(2)
                reader.seek(reader.tell()-4)
                printd(f'\t[bpp_debug] {deb}')
                printd(f'\t[bpp_debug_b2] {deb_b2}')

                alt_w = reader.read_int()
                if alt_w == 0 or alt_w % 2 != 0:
                    reader.seek(reader.tell()-2)
                    alt_w2 = reader.read_int(1)
                    reader.read_byte()
                    printd(f'\t\t[alt] Changing w={alt_w} to {alt_w2}')
                    alt_w = alt_w2

                alt_h = reader.read_int()
                if alt_h == 0 or alt_h % 2 != 0:
                    reader.seek(reader.tell()-2)
                    alt_h2 = reader.read_int(1)
                    reader.read_byte()
                    printd(f'\t\t[alt] Changing h={alt_h} to {alt_h2}')
                    alt_h = alt_h2

                # 8 bytes - Unknown
                wpg_unk2 = reader.read_int_array(4)
                printd(f'\t\tunk2={wpg_unk2}')

                bpp = reader.read_int()
                bpp_dupe = reader.read_int()

                if bpp == 8:
                    s1 = min(alt_w, width) if alt_w != 0 else width
                    s2 = min(alt_h, height) if alt_h != 0 else height

                    printd(f'\t\t[bpp8] Changing w={width} to {s1} and h={height} to {s2}')
                    width = s1
                    height = s2

                wpg_unk3 = reader.read_int_array(12, 1)
                reader.seek(reader.tell()-12)
                wpg_unk3_b2 = reader.read_int_array(6)

                printd(f'\t\tunk3={int_list_to_hex(wpg_unk3)}')
                printd(f'\t\tunk3_b2{int_list_to_hex(wpg_unk3_b2)}')
                # printd(f'\tw={width}, h={height}, altw={alt_w}, alth={alt_h}, unk2={wpg_unk2}, bpp={bpp}, bpp_dupe={bpp_dupe}, wpg_unk3={wpg_unk3}, tell={reader.tell()}')
                # assert bpp == bpp_dupe, f'{bpp}!={bpp_dupe}'

                all_shapes[i] = (width, height)
                all_bpps[i] = bpp
                all_alt_w[i] = alt_w
                all_alt_h[i] = alt_h
                all_wpg_unk3[i] = wpg_unk3

                D1 = 1024 if bpp==16 else 256
                filler += (width * height)+D1

            printd(f'WPG ALL INFO ENDS AT {reader.tell()}')
            # Test1
            # if file_idx==0:
            #     initial = reader.read(44)
            #     reader.seek(reader.tell()-44)
            #     joblib.dump(initial, 'figures2/initial.data')

            # # Test2
            wpg_offd = wpg_unk1_p2[1]
            all_wpg_offd.append(wpg_offd)

            printd(f'\tWant to add {wpg_offd} to offset')
            next_off = reader.total_bytes() if file_idx == len(offsets)-1 else offsets[file_idx+1]
            dn = next_off-(reader.tell()+filler)+wpg_offd
            printd(f'\tHow about {dn}=0x{dn:X}')

            if file_idx != len(offsets)-1:
                reader.seek(reader.tell()+dn)
            else:
                reader.seek(reader.tell()+dn-wpg_offd)

            predicted_rem_bytes = next_off-(reader.tell()+filler)
            printd(f'\tWe will be {predicted_rem_bytes} bytes away at the end')
            # assert predicted_rem_bytes%2==0
            # initial = reader.read_int_array(predicted_rem_bytes//2)
            # printd(f'\t\tInitial={initial}')

            # reader.read(reader.tell()+5000)

            # Test3
            # printd(f'NONZEROS {np.count_nonzero(wpg_header[:-4])}=={all_wpg_offd[file_idx]}')

            next_bpp = np.unique([val for _, val in all_bpps.items()])
            # assert len(next_bpp)==1, str(next_bpp)
            # next_bpp = next_bpp[0]

            for i in range(wpg_n_images):
                # if i == 0:
                #     reader.seek(1376)
                bpp_mode = all_bpps[i]
                shape = all_shapes[i]

                want = (shape[0]*shape[1])+D1
                printd(f'\t\tim={i}, w={shape[0]}, h={shape[1]}, tell={reader.tell()}/{reader.total_bytes()}=0x{reader.tell():X}/0x{reader.total_bytes():X}, want={want}, bpp={bpp_mode}')

                checkpt = reader.tell()
                im_data = reader.read(want)
                printd(f'\t\t\tData after {reader.tell()}=0x{reader.tell():X}')

                reader.seek(reader.total_bytes()-1024)
                dt2 = reader.read(1024)

                joblib.dump(im_data, f'{figures_dir}/{op_file.stem}_file{file_idx}_im{i}_bpp{bpp}.data')
                # joblib.dump(dt2, f'{figures_dir}/d2.data')
                reader.seek(checkpt+want)
                
                if not im_data:
                    ran_out_of_bytes.append(op_file)
                    printd('RAN OUT OF BYTES')
                    break
                
                after = reader.tell()
                im = Image.frombytes("P", shape, im_data, 'raw', 'P', 0, 0)
                # arr = np.array(im, dtype=np.uint8)
                # arr = np.roll(arr, (-wpg_offd, 0))
                # im = Image.fromarray(arr).convert('P')
                # im = im.transform(im.size, Image.AFFINE, (0, 0, 0, 0, 0, 0))

                # reader.read(256)

                pal_len = 1024
                # im.putpalette(reader.read(pal_len), 'RGBA')

                pal_offset = wpg_offd if predicted_rem_bytes < 0 else 0
                reader.seek(after-pal_len-pal_offset)
                arr = reader.read_int_array(pal_len, size_bytes=1)
                reader.seek(after)
                im.putpalette(arr, 'RGBA')

                im = im.convert('RGB')
                im.save(f'{figures_dir}/{op_file.stem}_file{file_idx}_im{i}_bpp{bpp}.png')
            
                if SHOW_FIGURES:
                    fig, curr = plt.subplots(figsize=(35, 35))
                    curr.set_xticklabels([])
                    curr.set_yticklabels([])
                    curr.imshow(im)
            
            rem = next_off-reader.tell()
            all_remains.append(rem)
            printd(f'\tFinished offset at {reader.tell()}/{reader.total_bytes()}=0x{reader.tell():X}/0x{reader.total_bytes():X}. Next offset {next_off} is {rem} bytes away')

        file.close()
    except Exception as ex:
        failed_files.append(op_file)
        exceptions.add(ex.__class__.__name__)
        if DEBUG or type(ex) == AssertionError:
            raise ex
        continue

if len(exceptions) > 0:
    print(exceptions)

print('Types', ALL_TYPES)

print('Remains', np.unique(all_remains))
printd(f'Remains {np.unique(all_remains)}')
if len(failed_files) > 0:
    print('Failed', len(failed_files))
if len(ran_out_of_bytes) > 0:
    print('Ran out of bytes', len(ran_out_of_bytes))

log_file.close()
# Remains [     0     76    140    172    204 165684]
# Failed 142
# Ran out of bytes 33


















# import io
# import pathlib
# import subprocess
# import multiprocess
# import copy

# import matplotlib.pyplot as plt
# import numpy as np
# from PIL import Image, ImageFile
# from tqdm import tqdm

# from core.io_util import FileStream
# from core.wpg import WPGFile

# if __name__ == "__main__":
#     op_file = pathlib.Path('textures/2D_LOAD_ELEVATOR.1E3EE6FB')

#     file = open(op_file, 'rb')
#     reader1 = FileStream(file)
#     all_bytes = reader1.read_remaining_bytes()
#     file.close()
    
#     reader = FileStream(io.BytesIO(all_bytes))

#     oop_header = reader.read_string(8)
#     file_size = reader.read_int(4)
#     unk1 = reader.read_byte_array(4)
#     count = reader.read_int(4)
#     print("There are", count, "files")

#     offsets = []

#     for _ in range(count):
#         offset = reader.read_int(4)
#         offsets.append(offset)
#         print(f"offset = {offset:X}")

#     file_size_dupe = reader.read_int(4)

#     all_shapes = {off: [] for off in offsets}
#     all_n_images = {off: -1 for off in offsets}


#     def process(i, i2):
#         with open('textures/2D_LOAD_ELEVATOR.1E3EE6FB', 'rb') as file:
#             reader = FileStream(file)
#             reader.seek(i)
#             arr = reader.read_int_array(768, size_bytes=1)

#             im = Image.open('original.png')
#             if max(arr) != 0:
#                 im.putpalette(arr, 'RGB')
#                 im.save(f'figures/{i}_rgb.png')

#             reader.seek(i)
#             arr = reader.read_int_array(1024, size_bytes=1)
#             if max(arr) != 0:
#                 im.putpalette(arr, 'RGBA')
#                 im.save(f'figures/{i}_rgba.png')

#     for file_idx, offset in enumerate(offsets):
#         all_extra_ints = {}
#         reader.seek(offset)
#         wpg_header = reader.read_byte_array(16)
#         wpg_temp = reader.read_string()

#         wpg_magic1 = reader.read_byte_array(20)

#         wpg_id = reader.read_string()

#         wpg_magic2 = reader.read_byte_array(4)

#         wpg_n_images = reader.read_int(4)
#         all_n_images[offset] = wpg_n_images

#         wpg_unk1 = reader.read_byte_array(84)
        
#         for i in range(wpg_n_images):
#             width = reader.read_int()
#             height = reader.read_int()

#             all_shapes[offset].append((width, height))
#             wpg_unk2 = reader.read_int_array(14)
#             all_extra_ints[i] = wpg_unk2
#             # wpg_unk2 = reader.read_byte_array(28)
#             print(offset, i, width, height, wpg_unk2)

#         data_start_offset = reader.tell()
#         print('Data starting at', data_start_offset)
#         for i in range(wpg_n_images):
#             shape = all_shapes[offset][i]
#             want = shape[0]*shape[1]

#             # elevator 1024 0 512 448 [256, 0, 0, 0, 2, 0, 16, 16, 33024, 3, 0, 0, 0, 0]
#             bpp_mode = all_extra_ints[i][6]
#             print(f'Currently idx={i}, tell={reader.tell()}/{reader.total_bytes()}, want={want}, bpp={bpp_mode}')
#             if bpp_mode == 8:
#                 s1 = min(all_extra_ints[i][0], shape[0])
#                 s2 = min(all_extra_ints[i][8], shape[1])
#                 shape = (s1, s2)
#             im_data = reader.read(shape[0]*shape[1])
#             if not im_data:
#                 print(f'Ran out of bytes')
#                 break
            
#             IM = Image.frombytes("P", shape, im_data, 'raw', 'P', 0, -1)
#             IM.save('original.png')

#             # images = [copy.deepcopy(IM) for _ in range(reader.total_bytes())]
#             idxs = list(range(reader.total_bytes()))
#             pbar = tqdm(total=len(idxs))

#             with multiprocess.Pool(5) as pool:
#                 for _ in pool.starmap(process, enumerate(idxs)):
#                     pbar.update(1)