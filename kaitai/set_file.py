# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class SetFile(ReadWriteKaitaiStruct):

    class EnemyState(IntEnum):
        inactive = 0
        active = 16256
    def __init__(self, is_file, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.is_file = is_file

    def _read(self):
        if self.is_file:
            self.header = SetFile.Header(self._io, self, self._root)
            self.header._read()

        self.num_enemies = self._io.read_u4le()
        self.header2 = self._io.read_bytes((60 if self.is_file else 20))
        self.enemies = []
        for i in range(self.num_enemies):
            _t_enemies = SetFile.Enemy(self._io, self, self._root)
            _t_enemies._read()
            self.enemies.append(_t_enemies)



    def _fetch_instances(self):
        if self.is_file:
            self.header._fetch_instances()

        for i in range(len(self.enemies)):
            self.enemies[i]._fetch_instances()

        pass


    def _write__seq(self, io=None):
        super(SetFile, self)._write__seq(io)
        if self.is_file:
            self.header._write__seq(self._io)

        self._io.write_u4le(self.num_enemies)
        self._io.write_bytes(self.header2)
        for i in range(len(self.enemies)):
            self.enemies[i]._write__seq(self._io)



    def _check(self):
        if self.is_file:
            if self.header._root != self._root:
                raise kaitaistruct.ConsistencyError(u"header", self.header._root, self._root)
            if self.header._parent != self:
                raise kaitaistruct.ConsistencyError(u"header", self.header._parent, self)

        if (len(self.header2) != (60 if self.is_file else 20)):
            raise kaitaistruct.ConsistencyError(u"header2", len(self.header2), (60 if self.is_file else 20))
        if (len(self.enemies) != self.num_enemies):
            raise kaitaistruct.ConsistencyError(u"enemies", len(self.enemies), self.num_enemies)
        for i in range(len(self.enemies)):
            if self.enemies[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"enemies", self.enemies[i]._root, self._root)
            if self.enemies[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"enemies", self.enemies[i]._parent, self)


    class Header(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.magic = self._io.read_bytes(3)
            if not (self.magic == b"\x4F\x53\x45"):
                raise kaitaistruct.ValidationNotEqualError(b"\x4F\x53\x45", self.magic, self._io, u"/types/header/seq/0")
            self.unused = self._io.read_bytes(5)
            self.file_size = self._io.read_u4le()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(SetFile.Header, self)._write__seq(io)
            self._io.write_bytes(self.magic)
            self._io.write_bytes(self.unused)
            self._io.write_u4le(self.file_size)


        def _check(self):
            if (len(self.magic) != 3):
                raise kaitaistruct.ConsistencyError(u"magic", len(self.magic), 3)
            if not (self.magic == b"\x4F\x53\x45"):
                raise kaitaistruct.ValidationNotEqualError(b"\x4F\x53\x45", self.magic, None, u"/types/header/seq/0")
            if (len(self.unused) != 5):
                raise kaitaistruct.ConsistencyError(u"unused", len(self.unused), 5)


    class Enemy(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.pad1 = self._io.read_bytes(4)
            self.angle = self._io.read_f4le()
            self.pad2 = self._io.read_bytes(2)
            self.unknown1 = self._io.read_bytes(2)
            self.pad3 = self._io.read_bytes(4)
            if not  (((self.pad3 == b"\x00\x00\x00\x00"))) :
                raise kaitaistruct.ValidationNotAnyOfError(self.pad3, self._io, u"/types/enemy/seq/4")
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()
            self.pad4 = self._io.read_bytes(2)
            if not (self.pad4 == b"\x00\x00"):
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00", self.pad4, self._io, u"/types/enemy/seq/8")
            self.state = KaitaiStream.resolve_enum(SetFile.EnemyState, self._io.read_u2le())
            self.category = self._io.read_bytes(4)
            self.pad5 = self._io.read_bytes(4)
            self.enemy_type = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode("UTF-8")
            self.pad6 = self._io.read_bytes(30)
            self.pad7 = self._io.read_bytes(2)
            if not (self.pad7 == b"\xB2\xFD"):
                raise kaitaistruct.ValidationNotEqualError(b"\xB2\xFD", self.pad7, self._io, u"/types/enemy/seq/14")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(SetFile.Enemy, self)._write__seq(io)
            self._io.write_bytes(self.pad1)
            self._io.write_f4le(self.angle)
            self._io.write_bytes(self.pad2)
            self._io.write_bytes(self.unknown1)
            self._io.write_bytes(self.pad3)
            self._io.write_f4le(self.x)
            self._io.write_f4le(self.y)
            self._io.write_f4le(self.z)
            self._io.write_bytes(self.pad4)
            self._io.write_u2le(int(self.state))
            self._io.write_bytes(self.category)
            self._io.write_bytes(self.pad5)
            self._io.write_bytes_limit((self.enemy_type).encode(u"UTF-8"), 8, 0, 0)
            self._io.write_bytes(self.pad6)
            self._io.write_bytes(self.pad7)


        def _check(self):
            if (len(self.pad1) != 4):
                raise kaitaistruct.ConsistencyError(u"pad1", len(self.pad1), 4)
            if (len(self.pad2) != 2):
                raise kaitaistruct.ConsistencyError(u"pad2", len(self.pad2), 2)
            if (len(self.unknown1) != 2):
                raise kaitaistruct.ConsistencyError(u"unknown1", len(self.unknown1), 2)
            if (len(self.pad3) != 4):
                raise kaitaistruct.ConsistencyError(u"pad3", len(self.pad3), 4)
            if not  (((self.pad3 == b"\x00\x00\x00\x00"))) :
                raise kaitaistruct.ValidationNotAnyOfError(self.pad3, None, u"/types/enemy/seq/4")
            if (len(self.pad4) != 2):
                raise kaitaistruct.ConsistencyError(u"pad4", len(self.pad4), 2)
            if not (self.pad4 == b"\x00\x00"):
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00", self.pad4, None, u"/types/enemy/seq/8")
            if (len(self.category) != 4):
                raise kaitaistruct.ConsistencyError(u"category", len(self.category), 4)
            if (len(self.pad5) != 4):
                raise kaitaistruct.ConsistencyError(u"pad5", len(self.pad5), 4)
            if (len((self.enemy_type).encode(u"UTF-8")) > 8):
                raise kaitaistruct.ConsistencyError(u"enemy_type", len((self.enemy_type).encode(u"UTF-8")), 8)
            if (KaitaiStream.byte_array_index_of((self.enemy_type).encode(u"UTF-8"), 0) != -1):
                raise kaitaistruct.ConsistencyError(u"enemy_type", KaitaiStream.byte_array_index_of((self.enemy_type).encode(u"UTF-8"), 0), -1)
            if (len(self.pad6) != 30):
                raise kaitaistruct.ConsistencyError(u"pad6", len(self.pad6), 30)
            if (len(self.pad7) != 2):
                raise kaitaistruct.ConsistencyError(u"pad7", len(self.pad7), 2)
            if not (self.pad7 == b"\xB2\xFD"):
                raise kaitaistruct.ValidationNotEqualError(b"\xB2\xFD", self.pad7, None, u"/types/enemy/seq/14")



