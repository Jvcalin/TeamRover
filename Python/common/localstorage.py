import serializer as ser
import os


class LocalStorage:

    def __init__(self, filename="localstorage.txt", path=os.getcwd()):
        self.filename = filename
        self.path = path
        self.content = ""
        self.fullpath = os.path.join(self.path, self.filename)
        self.items = {}

    def load(self):
        with open(self.fullpath, "rt") as f:
            self.content = f.read()
            self.items = ser.fromJSON(self.content)

    def save(self):
        with open(self.fullpath, "wt") as f:
            self.content = ser.toJSON(self.items)
            f.write(self.content)

