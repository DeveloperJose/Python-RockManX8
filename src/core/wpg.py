from PIL import Image

class Font:
    def __init__(self, path):
        textures =  self.__load_textures_from_file__(path)
        characters = self.__load_characters_from_textures__(textures)

        self.textures = textures
        self.characters = characters

    def text_bytes_to_im(self, raw_bytes):
        # Reduce gaps between characters by 5px
        COL_WIDTH = 15
        ROW_WIDTH = 20
        sentences, max_sentence_len = self.__split_bytes_to_sentences__(raw_bytes)
        cols = COL_WIDTH * max_sentence_len
        rows = ROW_WIDTH * len(sentences)
        im = Image.new('L', (cols, rows))
        for row_idx, sentence in enumerate(sentences):
            row_offset = row_idx * ROW_WIDTH
            for col_idx, char_byte in enumerate(sentence):
                col_offset = col_idx * COL_WIDTH
                # Get character image from list
                if char_byte >= len(self.characters):
                    im_curr_char = self.characters[0]
                else:
                    im_curr_char = self.characters[char_byte]

                # Paste into canvas
                im.paste(im_curr_char, (col_offset, row_offset))
        return im

    @staticmethod
    def __load_textures_from_file__(path):
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
                im_texture = im_raw_gray.crop((0, 0, 240, 240))
                textures.append(im_texture)

        return textures

    @staticmethod
    def __load_characters_from_textures__(textures):
        characters = []
        for texture in textures:
            # Extract all 144 characters from the texture
            for row in range(12):
                for col in range(12):
                    rstart = row * 20
                    rend = rstart + 20
                    cstart = col * 20
                    cend = cstart + 20
                    im_char = texture.crop((cstart, rstart, cend, rend))
                    characters.append(im_char)
        return characters

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