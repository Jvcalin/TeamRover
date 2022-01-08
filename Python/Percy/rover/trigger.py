

class trigger:

    def __init__(self):
        self.triggered = False

    def check(self):
        return False

    def do(self):
        self.triggered = True

    def reset(self):
        self.triggered = False


