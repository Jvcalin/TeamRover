"""This defines an interface to be implemented by percy and roger"""


class Robot:

    def __init__(self, mqtt):
        self.mode = "motor"
        self.direction = 0
        self.a = False
        self.b = False
        self.mqtt = mqtt

    def up(self):
        self.direction = 1
        self.tick()

    def down(self):
        self.direction = 5
        self.tick()

    def upleft(self):
        self.direction = 8
        self.tick()

    def upright(self):
        self.direction = 2
        self.tick()

    def left(self):
        self.direction = 7
        self.tick()

    def right(self):
        self.direction = 3
        self.tick()

    def downleft(self):
        self.direction = 6
        self.tick()

    def downright(self):
        self.direction = 4
        self.tick()

    def center(self):
        self.direction = 0
        self.tick()

    def a_press(self):
        self.a = True
        self.tick()

    def a_up(self):
        self.a = False
        self.tick()

    def b_press(self):
        self.b = True
        self.tick()

    def b_up(self):
        self.b = False
        self.tick()

    def toggle_mode(self):
        if self.mode == "motor":
            self.mode = "servo"
        else:
            self.mode = "motor"

    def tick(self):
        pass

