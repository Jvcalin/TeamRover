# Buttons
from adafruit_pybadger import pygamer
import WiFiMqtt

# button definitions
# up - forward
# down - reverse
# left/right - spin left/right
# center - stop
# up+left/right - swerve left/right (not implemented)
# back+left/right - swerve left/right (not implemented)

# a - beep
# b - swoopup
# start - power on/off (not implemented yet)
# select - switch devices (not implemented yet)

class MyPyGamer():
    def __init__(self, mqtt):
        self.me = pygamer.pygamer
        self.mqtt = mqtt
        self.motorfeed = mqtt.motor_cmd_feed
        self.beepfeed = mqtt.beep_cmd_feed
        self.values = {
            "direction": "Stop",
            "abutton": 0,
            "bbutton": 0,
            "startbutton": 0,
            "selectbutton": 0
        }

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

        if self.me.button.up:
            self.direction("Forward")
        elif self.me.button.down:
            self.direction("Reverse")
        elif self.me.button.left:
            self.direction("SpinLeft")
        elif self.me.button.right:
            self.direction("SpinRight")
        else:
            self.direction("Stop")

    def a_press(self):
        if self.values["abutton"] == 0:
            self.values["abutton"] = 1
            print("a press")

    def a_up(self):
        if self.values["abutton"] == 1:
            self.values["abutton"] = 0
            self.mqtt.publishMessage(self.beepfeed,"Beep")
            print("a up")

    def b_press(self):
        if self.values["bbutton"] == 0:
            self.values["bbutton"] = 1
            print("b press")

    def b_up(self):
        if self.values["bbutton"] == 1:
            self.values["bbutton"] = 0
            self.mqtt.publishMessage(self.beepfeed,"SwoopUp")
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
            print("select up")

    def direction(self, value):
        if self.values["direction"] != value:
            self.values["direction"] = value
            self.mqtt.publishMessage(self.motorfeed,value)
            print(value)
