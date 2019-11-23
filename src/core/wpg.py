import numpy as np
from PIL import Image


class Font:
    def __init__(self, path):
        self.wpg = WPGFile(path)

        characters = []
        for texture in self.wpg.textures:
            # Extract all 144 characters from the texture
            for row in range(12):
                for col in range(12):
                    rstart = row * 20
                    rend = rstart + 20
                    cstart = col * 20
                    cend = cstart + 20
                    im_char = texture[rstart:rend, cstart:cend]
                    characters.append(im_char)

        self.characters = np.array(characters)

    def text_bytes_to_array(self, raw_bytes):
        sentences, max_sentence_len = self.__split_to_sentences__(raw_bytes)
        cols = 20 * max_sentence_len
        rows = 20 * len(sentences)
        im = np.zeros((rows, cols))
        for row_idx, sentence in enumerate(sentences):
            row_start = row_idx * 20
            row_end = row_start + 20
            for col_idx, char_byte in enumerate(sentence):
                if char_byte >= len(self.characters):
                    im_curr_char = self.characters[0]
                else:
                    im_curr_char = self.characters[char_byte]
                col_start = col_idx * 20
                col_end = col_start + 20
                im[row_start:row_end, col_start:col_end] = im_curr_char

        return im

    @staticmethod
    def __split_to_sentences__(raw_bytes):
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


class WPGFile:
    def __init__(self, path=None):
        self.textures = None
        self.path = None

        if path is not None:
            self.path = path
            self.__load_from_file__(path)

    def __load_from_file__(self, path):
        textures = []
        with open(path, 'rb') as file:
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
                im_texture = np.array(im_raw_gray)[:240, :240]
                textures.append(im_texture)

        self.textures = textures