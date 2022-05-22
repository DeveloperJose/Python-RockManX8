from tqdm import tqdm
from typing import List

from core.io_util import FileStream
import core.constants as constants


class SetEnemy:
    def __init__(self):
        self.u1 = None
        self.id = 0
        self.u2 = None
        self.x = 0.0
        self.y = 0.0
        self.fvar1 = 0.0
        self.fvar2 = 0.0
        self.k1 = 0
        self.u4 = None
        self.type = ""
        self.u5 = None

    @classmethod
    def from_reader(cls, reader):
        instnc = cls()

        u1 = reader.read_int_array(3)  # 6 bytes
        enemy_id = reader.read_int()  # 2 bytes (0x6)
        u2 = reader.read_int_array(4)  # 8 bytes (0x8)
        enemy_x = reader.read_float()  # 4 bytes (0x10)
        enemy_y = reader.read_float()  # 4 bytes (0x14)

        # 8 bytes
        fvar1 = reader.read_float() # 4 bytes bytes (0x18)
        fvar2 = reader.read_float() # 4 bytes (0x1C)

        k1 = reader.read_int()  # 2 bytes (0x20)
        u4 = reader.read_int_array(3)  # 6 bytes (0x22)
        enemy_type = reader.read_string(8)  # 8 bytes (0x28)
        u5 = reader.read_int_array(16)  # 32 bytes (0x30)

        instnc.u1 = u1
        instnc.id = enemy_id
        instnc.u2 = u2
        instnc.x = enemy_x
        instnc.y = enemy_y
        instnc.fvar1 = fvar1
        instnc.fvar2 = fvar2
        instnc.k1 = k1
        instnc.u4 = u4
        instnc.type = enemy_type
        instnc.u5 = u5
        return instnc

    def write_to_stream(self, writer: FileStream):
        writer.write_int_array(self.u1)
        writer.write_int(self.id)
        writer.write_int_array(self.u2)
        writer.write_float(self.x)
        writer.write_float(self.y)
        writer.write_float(self.fvar1)
        writer.write_float(self.fvar2)
        writer.write_int(self.k1)
        writer.write_int_array(self.u4)
        writer.write_string(self.type, pad_bytes=8)
        writer.write_int_array(self.u5)

    def get_header(self):
        s = "IDX".ljust(3) + " , "
        s += "U1".ljust(len(self.u1) * 6 - 1) + " , "
        s += "ID".ljust(5) + " ,"
        s += "U2".ljust(len(self.u2) * 6 - 1) + " , "

        s += "X".ljust(8) + " , "
        s += "Y".ljust(8) + " , "

        s += "FV1".ljust(8) + " , "
        s += "FV2".ljust(8) + " , "

        s += "K1".ljust(5) + " , "
        s += "U4".ljust(len(self.u4) * 6 - 1) + " , "
        s += "Type".ljust(8) + " , "
        s += "U5".ljust(len(self.u5) * 6 - 1)
        return s

    def print(self, idx):
        s = str(idx).ljust(3) + " ,"
        s += FileStream.int_array_to_hex(self.u1) + " , "
        s += FileStream.int_to_hex(self.id) + " , "
        s += FileStream.int_array_to_hex(self.u2) + " , "

        s += f'{self.x:.1f}'.ljust(8) + " , "
        s += f'{self.y:.1f}'.ljust(8) + " , "
        s += f'{self.fvar1:.1f}'.ljust(8) + " , "
        s += f'{self.fvar2:.1f}'.ljust(8) + " , "
        # s += FileStream.float_to_hex(self.y) + ","
        # s += FileStream.int_array_to_hex(self.u3) + ","
        s += FileStream.int_to_hex(self.k1) + " , "
        s += FileStream.int_array_to_hex(self.u4) + " , "
        s += self.type.rjust(8) + " , "
        s += FileStream.int_array_to_hex(self.u5)
        print(s)

    def __lt__(self, other):
        return self.prm_number() < other.prm_number()

    def prm_number(self):
        return int(self.type[3:])

    def __repr__(self):
        return self.type

    def id_bytes(self):
        s = ''
        # s += FileStream.int_array_to_hex(self.u1) + ' '
        # s += FileStream.int_to_hex(self.id) + ' '
        # s += FileStream.int_array_to_hex(self.u2) + ' '
        s += FileStream.float_to_hex(self.x) + ' '
        s += FileStream.float_to_hex(self.y) + ' '
        # s += FileStream.int_array_to_hex(self.u3) + ' '
        # s += FileStream.int_to_hex(self.k1) + ' '
        # s += FileStream.int_array_to_hex(self.u4) + ' '
        # s += FileStream.str_to_hex(self.type) + ' '
        # s += FileStream.int_array_to_hex(self.u5)
        return s


class SetFile:
    enemies: List[SetEnemy]

    def __init__(self, path=None):
        self.enemies = []
        if path is not None:
            self.path = path
            self.__load_from_file__(path)

    @property
    def stage_name(self):
        if self.path is None:
            return "Unknown Stage"

        for stage_id in constants.STAGE_NAMES.keys():
            set_id = "Set" + stage_id
            if set_id in self.path:
                return constants.STAGE_NAMES[stage_id]

        return "Unknown Stage"

    def __load_from_file__(self, spath):
        with open(spath, 'rb') as file:
            reader = FileStream(file)

            num_enemies = reader.read_int()
            # Handle ARC format
            if num_enemies == 0x534F:
                print('ARC file')
                h1 = reader.read_int_array(5)
                num_enemies = reader.read_int()

            # Regular Header (0x40 bytes)
            rest_of_header = reader.read_string(0x3E)

            # Enemy Data (0x50=80 bytes each)
            for i in tqdm(range(num_enemies)):
                enemy = SetEnemy.from_reader(reader)
                self.enemies.append(enemy)

    def save(self, spath=None):
        if spath is None:
            spath = self.path

        with open(spath, 'wb') as file:
            writer = FileStream(file)

            writer.write_int(len(self.enemies))
            writer.write_int_array([0] * 31)

            for enemy in self.enemies:
                enemy.write_to_stream(writer)

    def print(self):
        print(self.enemies[0].get_header())
        for idx, enemy in enumerate(self.enemies):
            enemy.print(idx)