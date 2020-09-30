import json
import os
import triggers


class LocalStorage:

    def __init__(self, filename="localstorage.txt", path=os.getcwd()):
        self.filename = filename
        self.path = path
        self.fullpath = os.path.join(self.path, self.filename)
        self.items = {}

    def load(self):
        with open(self.fullpath, "rt") as f:
            self.items = json.loads(f.read())

    def save(self):
        with open(self.fullpath, "wt") as f:
            f.write(json.dumps(self.items))


