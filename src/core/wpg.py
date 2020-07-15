# 537 files different -> 29 files different
import io
from pathlib import Path
from typing import List

from PIL import Image

from core.io_util import FileStream

WPG_HEADER_SIZE = 32
RGBA_HEADER_SIZE = 18
P_HEADER_SIZE = 786
RGBA_BYTES_PER_PIXEL = 4
P_BYTES_PER_PIXEL = 1


class WPGFile:
    path: Path
    header: List[int]
    textures: List[Image.Image]

    def __init__(self, path: Path):
        self.path = path
        self.header = []
        self.textures = []
        self.unparsed_bytes = b''
        self.__load_from_file__(path)

    def __load_from_file__(self, path: Path):
        with open(path, 'rb') as file:
            reader = FileStream(file)
            self.__load_header__(reader)
            self.__load_textures__(reader)

    def __load_header__(self, reader: FileStream):
        self.header = reader.read_byte_array(WPG_HEADER_SIZE)

    def __load_textures__(self, reader: FileStream):
        while True:
            if reader.finished_reading():
                break

            offset = reader.tell()
            im_data = io.BytesIO(reader.read_remaining_bytes())
            try:
                # Load image, flip it, and store it
                im: Image.Image = Image.open(im_data)
                # im = im.transpose(Image.FLIP_TOP_BOTTOM)
                self.textures.append(im)

                # Figure out where exactly the next image begins
                if im.mode == "RGBA":
                    bytes_per_pixel = RGBA_BYTES_PER_PIXEL
                    im_header_size = RGBA_HEADER_SIZE
                elif im.mode == "P":
                    bytes_per_pixel = P_BYTES_PER_PIXEL
                    im_header_size = P_HEADER_SIZE

                size = (im.width * im.height * bytes_per_pixel) + im_header_size
                reader.seek(offset + size)
                print("Size: ", size, " and Mode:", im.mode)
                print("Current Offset: ", reader.tell(), ", File Size: ", reader.total_bytes())
            except IOError:
                print("Couldn't read image")
                break

        if not reader.finished_reading():
            self.unparsed_bytes = reader.read_remaining_bytes()
            print("Unparsed Bytes", len(self.unparsed_bytes))

    def save(self, spath: Path = None):
        if spath is None:
            spath = self.path

        with open(spath, 'wb') as file:
            writer = FileStream(file)
            writer.write_byte_array(self.header)

            for im_texture in self.textures:
                # orig_im = im_texture.transpose(Image.FLIP_TOP_BOTTOM)
                orig_im = im_texture
                with io.BytesIO() as io_bytes:
                    orig_im.save(io_bytes, format="TGA")
                    io_bytes.getbuffer()[17] = 8
                    im_bytes = io_bytes.getvalue()[:-26]
                    writer.write(im_bytes)
                    print("Flag: ", io_bytes.getvalue()[17])

            writer.write(self.unparsed_bytes)
        print("Saved to", spath)

    def export_to_folder(self, folder_path: Path):
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
        for idx, texture in enumerate(self.textures):
            texture_filename = f'{idx}.tga'
            texture.save(folder_path / texture_filename)

    def import_from_folder(self, folder_path: Path):
        textures = []
        for texture_path in folder_path.glob("*.tga"):
            im_texture: Image.Image = Image.open(texture_path)
            textures.append(im_texture)

        print("Imported", len(textures), "from", folder_path)
        self.textures = textures

    def close(self):
        for tex in self.textures:
            tex.close()


class Font(WPGFile):
    characters: List[Image.Image]

    def __init__(self, path):
        super().__init__(path)
        self.characters = []
        self.__load_characters_from_textures__()

    def __load_characters_from_textures__(self):
        for texture in self.textures:
            # Extract all 144 characters from the texture
            for row in range(12):
                for col in range(12):
                    rstart = row * 20
                    rend = rstart + 20
                    cstart = col * 20
                    cend = cstart + 20

                    im_char = texture.crop((cstart, rstart, cend, rend))
                    self.characters.append(im_char)
        return self.characters

    def get_character_image(self, char_byte):
        # Get character image from list (if possible) or default to blank
        if char_byte >= len(self.characters) or char_byte < 0:
            return self.characters[0]
        else:
            return self.characters[char_byte]

    def text_bytes_to_image(self, raw_bytes):
        # Reduce gaps between characters by 5px
        COL_WIDTH = 15
        ROW_WIDTH = 20

        # Split bytes into multiple lines / sentences
        sentences, max_sentence_len = self.__split_bytes_to_sentences__(raw_bytes)

        # Prepare blank image to fit all the characters in it
        cols = COL_WIDTH * max_sentence_len
        rows = ROW_WIDTH * len(sentences)
        im = Image.new('L', (cols, rows))

        for row_idx, sentence in enumerate(sentences):
            row_offset = row_idx * ROW_WIDTH
            for col_idx, char_byte in enumerate(sentence):
                col_offset = col_idx * COL_WIDTH
                im_curr_char = self.get_character_image(char_byte)
                # Paste into canvas
                im.paste(im_curr_char, (col_offset, row_offset))
        return im

    @staticmethod
    def __split_bytes_to_sentences__(raw_bytes):
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


if __name__ == '__main__':
    import filecmp
    import shutil

    #%%
    wpg_dir = Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\opk')
    temp_path = Path('temp')
    shutil.rmtree(temp_path, ignore_errors=True)
    diff_files = []
    for filepath in wpg_dir.rglob("*.wpg"):
        if 'temp' in filepath.name:
            continue
        test_wpg = WPGFile(filepath)
        test_wpg.export_to_folder(temp_path)
        test_wpg.import_from_folder(temp_path)
        test_wpg.save('temp.wpg')
        test_wpg.close()

        # Compare binaries to see if they are different
        if not filecmp.cmp(filepath,  'temp.wpg', shallow=False):
            print('************************* Different File: ', filepath)
            diff_files.append(str(filepath))

        # Clean-up temp folder
        shutil.rmtree(temp_path)

    print("********** All Different Files **********")
    print("Length: ", len(diff_files))
    for filename in diff_files:
        print(filename)

    #%%
    w = WPGFile(Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\opk\title\wpg\2D_LOAD_ATARI00_ID_2D_100.wpg'))
    testing_path = Path(r'C:\Users\xeroj\Desktop\Programs\noesisv4428\x8_testing')
    w.export_to_folder(testing_path / 'testing')
    w.import_from_folder(testing_path / 'testing')
    shutil.rmtree(testing_path / 'testing', ignore_errors=True)
    w.save(testing_path / "test.wpg")
    print('Same file: ', filecmp.cmp(testing_path / "test.wpg",  w.path, shallow=False))