# Buttons
from adafruit_pybadger import pygamer
import WiFiMqtt

#https://circuitpython.readthedocs.io/projects/pybadger/en/latest/

# button definitions
# up - forward
# down - reverse
# left/right - spin left/right
# center - stop
# up+left/right - swerve left/right
# back+left/right - swerve left/right

# a - go faster
# b - go slower
# start - power on/off (not implemented yet)
# select - switch devices (not implemented yet)

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

class MyPyGamer():
    def __init__(self, mqtt):
        self.me = pygamer.pygamer
        self.mqtt = mqtt
        self.motorfeed = mqtt.motor_cmd_feed
        self.beepfeed = mqtt.beep_cmd_feed
        self.servofeed = mqtt.servo_cmd_feed
        self.values = {
            "direction": "Stop",
            "abutton": 0,
            "bbutton": 0,
            "startbutton": 0,
            "selectbutton": 0
        }
        self.mode = "motor"
        self.pygamerNeoPixels().fill(RED)
        self.pygamerNeoPixels().brightness = 0.02

    def pygamerNeoPixels(self):
        return self.me.pixels

    def checkButtons(self):
        if self.me.button.a:
            self.a_press()
        else:
            self.a_up()
        if self.me.button.b:
            self.b_press()
        else:
            self.b_up()
        if self.me.button.start:
            self.start_press()
        else:
            self.start_up()
        if self.me.button.select:
            self.select_press()
        else:
            self.select_up()

        if self.mode == "motor":
            if self.me.button.up and self.me.button.left:
                self.direction("TurnLeft")
            elif self.me.button.up and self.me.button.right:
                self.direction("TurnRight")
            elif self.me.button.down and self.me.button.left:
                self.direction("ReverseLeft")
            elif self.me.button.down and self.me.button.right:
                self.direction("ReverseRight")
            elif self.me.button.up:
                self.direction("Forward")
            elif self.me.button.down:
                self.direction("Reverse")
            elif self.me.button.left:
                self.direction("SpinLeft")
            elif self.me.button.right:
                self.direction("SpinRight")
            else:
                self.direction("Stop")
        elif self.mode == "servo":
            if self.me.button.up:
                self.direction("U15")
            elif self.me.button.down:
                self.direction("D15")
            elif self.me.button.left:
                self.direction("L15")
            elif self.me.button.right:
                self.direction("R15")
            else:
                self.direction("")

    def a_press(self):
        if self.values["abutton"] == 0:
            self.values["abutton"] = 1
            print("a press")

    def a_up(self):
        if self.values["abutton"] == 1:
            self.values["abutton"] = 0
            if self.mode == "motor":
                self.direction("GoFaster")
            elif self.mode == "servo":
                self.direction("Reset")
            print("a up")

    def b_press(self):
        if self.values["bbutton"] == 0:
            self.values["bbutton"] = 1
            print("b press")

    def b_up(self):
        if self.values["bbutton"] == 1:
            self.values["bbutton"] = 0
            if self.mode == "motor":
                self.direction("GoSlower")
            elif self.mode == "servo":
                self.direction("Reset")
            print("b up")

    def start_press(self):
        if self.values["startbutton"] == 0:
            self.values["startbutton"] = 1
            print("start press")

    def start_up(self):
        if self.values["startbutton"] == 1:
            self.values["startbutton"] = 0
            print("start up")

    def select_press(self):
        if self.values["selectbutton"] == 0:
            self.values["selectbutton"] = 1
            print("select press")

    def select_up(self):
        if self.values["selectbutton"] == 1:
            self.values["selectbutton"] = 0
            self.switchmode()
            print("select up")

    def direction(self, value):
        if self.values["direction"] != value:
            self.values["direction"] = value
            if self.mode == "motor":
                self.mqtt.publishMessage(self.motorfeed, value)
            elif self.mode == "servo":
                if value != "":
                    self.mqtt.publishMessage(self.servofeed, value)
            print(value)

    def switchmode(self):
        if self.mode == "motor":
            self.direction("stop")
            self.mode = "servo"
            self.pygamerNeoPixels().fill(BLUE)
        elif self.mode == "servo":
            self.direction("reset")
            self.mode = "motor"
            self.pygamerNeoPixels().fill(GREEN)
