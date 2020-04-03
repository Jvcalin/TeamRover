



class Sensors:
    def __init__(self):
        self.imu = Imu()


class Imu:
    def __init__(self):
        self.accel_x = 12
        self.accel_y = 12
        self.accel_z = 12
        self.gyro_x = 23
        self.gyro_y = 23
        self.gyro_z = 23
        self.tilt = 23
        self.roll = 23
        self.yaw = 23



class Led:
    def __init__(self):
        pass
    def set(self):
        pass
    def set(self,color):
        pass

    
led = Led()
sensors = Sensors()

# [{'r':12, 'g':12, 'b':21, 'w' :12},
# {'r':12, 'g':12, 'b':21, 'w' :12},
# {'r':12, 'g':12, 'b':21, 'w' :12}
# ]