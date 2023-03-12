import json

from typing import NamedTuple


class Setting:

    def __init__(self, file: str, receiver: list, sender: str, password: str):
        self.file = file
        self.receiver = receiver
        self.sender = sender
        self.password = password

    def save(self, _file=None):
        if _file is None:
            _file = self.file
        with open(self.file, mode="r+") as f:
            f.write(json.dumps(self.__dict__))
            print(json.dumps(self.__dict__))