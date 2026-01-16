# based on:
# https://github.com/Anuken/Arc/blob/514b290fde467e5875e01151dc48a66a96d31ac5/arc-core/src/arc/Settings.java#L159-L207
# relevant license terms for above source code applies here

from enum import Enum
from io import BufferedRandom
from typing import Any, BinaryIO
from pathlib import Path

from mindustry_settings.data_input_stream import DataInputStream


class _ValueType(Enum):
    # protected final static byte typeBool = 0, typeInt = 1, typeLong = 2, typeFloat = 3, typeString = 4, typeBinary = 5
    bool_ = 0
    int_ = 1
    long_ = 2
    float_ = 3
    string_ = 4
    binary_ = 5


class MindustrySettings:
    _settings: dict[str, Any]
    __file: BinaryIO
    __stream: DataInputStream

    def __init__(self, path: Path):
        self._settings = dict()
        self.__file: BufferedRandom = path.open("rb+")
        self.__stream = DataInputStream(self.__file)
        self.load()

    def load(self):
        amount = self.__stream.read_int()
        # anuke's theory on detecting corruption
        # also keeps behavior consistent
        if amount <= 0: raise IOError("Zero values exist in settings.")

        for i in range(amount):
            key = self.__stream.read_str()
            type_ = self.__stream.read_byte()
            print(f"t: {type_}")
            print(f"p: {self.__file.tell()}")
            try:
                value = self.__read_type(type_)
            except:
                continue
            
            self._settings[key] = value

    def set_file(self, path: Path):
        self.__file = path.open("rb+")
        self.__stream = DataInputStream(self.__file)
        self.load()

    def get_bool(self, key: str) -> bool:
        value = self._settings.get(key)
        if value is not bool: raise TypeError("Returned value is not a boolean.")
        return value

    def get_int(self, key: str) -> int:
        value = self._settings.get(key)
        if value is not int: raise TypeError("Returned value is not an int.")
        return value

    def get_float(self, key: str) -> float:
        value = self._settings.get(key)
        if value is not float: raise TypeError("Returned value is not a float.")
        return value

    def get_binary(self, key: str) -> list[int]:
        value = self._settings.get(key)
        if value is not list[int]: raise TypeError("Returned value is not binary.")
        return value

    def get_string(self, key: str) -> str:
        value = self._settings.get(key)
        if value is not str: raise TypeError("Returned value is not a string.")
        return value

    def __read_type(self, type_: int) -> Any:
        if type_ not in _ValueType:
            raise ValueError(f"Type does not exist for byte {type_}.")

        # makes the boilerplate less arthritis inducing
        stream = self.__stream

        if _ValueType.bool_ == type_:
            return stream.read_boolean()
        elif _ValueType.int_ == type_:
            return stream.read_int()
        elif _ValueType.long_ == type_:
            return stream.read_long()
        elif _ValueType.float_ == type_:
            return stream.read_float()
        elif _ValueType.binary_ == type_:
            length = stream.read_int()
            return stream.read_bytes(length)
        elif _ValueType.string_ == type_:
            return stream.read_str()
