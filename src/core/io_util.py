import re
import struct


class FileStream():
    def __init__(self, file):
        self.__file__ = file

    def tell(self):
        return self.__file__.tell()

    def total_bytes(self):
        prev_pos = self.tell()
        self.__file__.seek(0, 2)
        buf_size = self.tell()
        self.seek(prev_pos)
        return buf_size

    def finished_reading(self):
        return self.tell() >= self.total_bytes()

    def seek(self, offset):
        self.__file__.seek(offset)

    def read(self, n_bytes):
        r_byte = self.__file__.read(n_bytes)
        if len(r_byte) != n_bytes:
            return False
        return r_byte

    def read_remaining_bytes(self):
        return self.__file__.read(self.total_bytes())

    def read_byte(self):
        raw = self.__file__.read(1)
        if len(raw) != 1:
            return False
        return raw

    def read_int(self, size_bytes=2):
        raw = self.__file__.read(size_bytes)
        if len(raw) != size_bytes:
            return False
        return int.from_bytes(raw, byteorder='little')

    def read_float(self, size_bytes=4):
        raw = self.__file__.read(size_bytes)
        return struct.unpack('<f', raw)[0]

    def read_string(self, size_bytes=16):
        raw = self.__file__.read(size_bytes)
        decoded_str = raw.decode('utf-8', errors='replace')
        decoded_str = re.sub(r'[\x00-\x2F]', r'', decoded_str)
        return decoded_str

    def read_byte_array(self, num_bytes):
        arr = []
        for i in range(num_bytes):
            raw_byte = self.read_byte()
            if raw_byte is not False:
                arr.append(raw_byte)
        return arr

    def read_int_array(self, num_ints):
        arr = []
        for i in range(num_ints):
            int_byte = self.read_int()
            if int_byte is not False:
                arr.append(int_byte)
        return arr

    def write(self, bytes):
        self.__file__.write(bytes)

    def write_int(self, i):
        int_bytes = i.to_bytes(2, byteorder='little')
        self.__file__.write(int_bytes)

    def write_float(self, f):
        float_bytes = struct.pack("<f", f)
        self.__file__.write(float_bytes)

    def write_string(self, s, pad_bytes=16):
        str_bytes = str.encode(s)
        self.__file__.write(str_bytes)

        # Pad missing bytes with 0
        missing_bytes = max(pad_bytes - len(s), 0)
        for i in range(missing_bytes):
            self.__file__.write(b'\0')

    def write_byte_array(self, arr):
        for by in arr:
            self.__file__.write(by)

    def write_int_array(self, arr):
        for n in arr:
            self.write_int(n)

    def write_string_array(self, arr):
        for st in arr:
            self.write_string(st)

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