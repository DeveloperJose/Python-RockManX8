from PIL import Image
from core.io_util import FileStream
from typing import List


class WPGFile:
    path: str
    header: List[int]
    textures: List[Image.Image]

    def __init__(self, path):
        self.path = path
        self.header = []
        self.textures = []
        self.__load_from_file__(path)

    def save(self, spath=None):
        if spath is None:
            spath = self.path

        with open(spath, 'wb') as file:
            writer = FileStream(file)
            writer.write_byte_array(self.header)

            for im_texture in self.textures:
                writer.write_byte_array([b'\x00', b'\x00', b'\x02', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00'])
                writer.write_int(im_texture.width)
                writer.write_int(im_texture.height)
                writer.write_int(2080)

                im_bgr: Image.Image = WPGFile.rgba_to_bgra(im_texture)
                im_bytes = im_bgr.tobytes('raw')
                writer.write(im_bytes)

    def __load_from_file__(self, path):
        with open(path, 'rb') as file:
            reader = FileStream(file)
            self.__load_header__(reader)
            self.__load_textures__(reader)

    def __load_header__(self, reader):
        self.header = reader.read_byte_array(0x20)

    def __load_textures__(self, reader):
        while True:
            im_header = reader.read_byte_array(12)
            if len(im_header) != 12:
                break
            im_width = reader.read_int()
            im_height = reader.read_int()
            im_extra_int = reader.read_int()
            im_data = reader.read(im_width * im_height * 4)

            print(f"im_h{im_header},im_hh={im_extra_int}")

            # Create BGR image from data, then convert to RGB
            im_bgra = Image.frombytes('RGBA', (im_width, im_height), im_data)
            im = WPGFile.bgra_to_rgba(im_bgra)

            self.textures.append(im)

    @staticmethod
    def bgra_to_rgba(im_bgra: Image.Image):
        blue, green, red, alpha = im_bgra.split()
        return Image.merge("RGBA", (red, green, blue, alpha))

    @staticmethod
    def rgba_to_bgra(im_rgba: Image.Image):
        red, green, blue, alpha = im_rgba.split()
        return Image.merge("RGBA", (blue, green, red, alpha))


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