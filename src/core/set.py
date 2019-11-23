from core.io import FileStream
import core.constants as Const

class SetEnemy:
    def __init__(self):
        self.u1 = None
        self.id = 0
        self.u2 = None
        self.x = 0.0
        self.y = 0.0
        self.u3 = None
        self.k1 = 0
        self.u4 = None
        self.type = ""
        self.u5 = None

    @classmethod
    def from_reader(cls, reader):
        instnc = cls()

        u1 = reader.read_int_array(3)  # 6 bytes
        enemy_id = reader.read_int()  # 2 bytes
        u2 = reader.read_int_array(4)  # 8 bytes
        enemy_x = reader.read_float()  # 4 bytes
        enemy_y = reader.read_float()  # 4 bytes
        u3 = reader.read_int_array(4)  # 8 bytes
        k1 = reader.read_int()  # 2 bytes
        u4 = reader.read_int_array(3)  # 6 bytes
        enemy_type = reader.read_string(8)  # 8 bytes
        u5 = reader.read_int_array(16)  # 32 bytes

        instnc.u1 = u1
        instnc.id = enemy_id
        instnc.u2 = u2
        instnc.x = enemy_x
        instnc.y = enemy_y
        instnc.u3 = u3
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
        writer.write_int_array(self.u3)
        writer.write_int(self.k1)
        writer.write_int_array(self.u4)
        writer.write_string(self.type, pad_bytes=8)
        writer.write_int_array(self.u5)

    def get_header(self):
        s = "IDX".ljust(3) + ","
        s += "U1".ljust(len(self.u1) * 5 - 1) + ","
        s += "ID".ljust(4) + ","
        s += "U2".ljust(len(self.u2) * 5 - 1) + ","
        s += "U3".ljust(len(self.u3) * 5 - 1) + ","
        s += "K1".ljust(4) + ","
        s += "U4".ljust(len(self.u4) * 5 - 1) + ","
        s += "Type".ljust(8) + ","
        s += "U5".ljust(len(self.u5) * 5 - 1)
        return s

    def print(self, idx):
        s = str(idx).ljust(3) + ","
        s += FileStream.int_array_to_hex(self.u1) + ","
        s += FileStream.int_to_hex(self.id) + ","
        s += FileStream.int_array_to_hex(self.u2) + ","
        # s += FileStream.float_to_hex(self.x) + ","
        # s += FileStream.float_to_hex(self.y) + ","
        s += FileStream.int_array_to_hex(self.u3) + ","
        s += FileStream.int_to_hex(self.k1) + ","
        s += FileStream.int_array_to_hex(self.u4) + ","
        s += self.type.rjust(8) + ","
        s += FileStream.int_array_to_hex(self.u5) + ","
        print(s)


class SetFile:
    def __init__(self, path=None):
        self.enemies = []
        if path is not None:
            self.path = path
            self.__load_from_file__(path)

    @property
    def stage_name(self):
        if self.path is None:
            return "Unknown Stage"

        for stage_id in Const.STAGE_NAMES.keys():
            set_id = "Set" + stage_id
            if set_id in self.path:
                return Const.STAGE_NAMES[stage_id]

        return "Unknown Stage"

    def __load_from_file__(self, spath):
        with open(spath, 'rb') as file:
            reader = FileStream(file)

            # Header (0x40 bytes)
            num_enemies = reader.read_int()
            rest_of_header = reader.read_string(0x3E)

            # Enemy Data (0x50=80 bytes each)
            for i in range(num_enemies):
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