import robot


class Roger(robot.Robot):

    def __init__(self, mqtt, refresh_func):
        self.mqtt = mqtt
        self.name = "Roger"