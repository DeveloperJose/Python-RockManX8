import re
import struct


class FileStream:
    def __init__(self, file):
        self.file = file

    def read_string(self, size_bytes=16):
        raw = self.file.read(size_bytes)
        decoded_str = raw.decode('utf-8', errors='replace')
        decoded_str = re.sub(r'[\x00-\x2F]', r'', decoded_str)
        return decoded_str

    def read_int(self, size_bytes=2):
        raw = self.file.read(size_bytes)
        return int.from_bytes(raw, byteorder='little')

    def read_int_array(self, num_ints):
        arr = []
        for i in range(num_ints):
            arr.append(self.read_int())
        return arr

    def read_float(self, size_bytes=4):
        raw = self.file.read(size_bytes)
        return struct.unpack('<f', raw)[0]

    def tell(self):
        return self.file.tell()

    def seek(self, offset):
        self.file.seek(offset)

    def write_string(self, s, pad_bytes=16):
        str_bytes = str.encode(s)
        self.file.write(str_bytes)

        # Pad missing bytes with 0
        missing_bytes = max(pad_bytes - len(s), 0)
        for i in range(missing_bytes):
            self.file.write(b'\0')

    def write_float(self, f):
        float_bytes = struct.pack("<f", f)
        self.file.write(float_bytes)

    def write_int(self, i):
        int_bytes = i.to_bytes(2, byteorder='little')
        self.file.write(int_bytes)

    def write_string_array(self, arr):
        for s in arr:
            self.write_string(s)

    def write_int_array(self, arr):
        for i in arr:
            self.write_int(i)

    @staticmethod
    def int_array_to_hex(arr):
        hexes = []
        # Little-Endian order is reversed
        for n in arr:
            hexes.append(FileStream.int_to_hex(n))
        return ",".join(hexes)

    @staticmethod
    def int_to_hex(n):
        # Convert to hex
        hex_str = hex(n)
        # Remove 0x
        hex_str = hex_str[2:]
        # Reverse
        p1 = hex_str[0:2]
        p2 = hex_str[2:4]
        # Pad
        return (p2 + p1).ljust(4, '_')

    @staticmethod
    def float_to_hex(f):
        # Convert to hex
        hex_str = hex(struct.unpack('<I', struct.pack('<f', f))[0])
        # Remove 0x and e##
        hex_str = hex_str[2:-3]
        # Reverse
        p1 = hex_str[0:2]
        p2 = hex_str[2:4]
        p3 = hex_str[4:6]
        p4 = hex_str[6:8]
        # Pad
        return (p4 + p3 + p2 + p1).ljust(8, '_')