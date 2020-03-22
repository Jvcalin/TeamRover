
"""
ProxSensors = { "front":Matrix.ProxSensor(0), 
                "left":Matrix.ProxSensor(45), 
                "right":Matrix.ProxSensor(-45), 
                "back":Matrix.ProxSensor(180)}
"""



class ProxSensor:

    def __init__(self, angle):
        self.angle = angle  #angle is the direction of the sensor in relation to the orientation
        self.value = 0

    def read(self):
        return self.value



