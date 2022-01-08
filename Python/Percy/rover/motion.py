import board
import broadcast
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX


print("Initializing accelerometer")
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = LSM6DSOX(i2c)
print("Accelerometer ready")

def tick():
    broadcast.send("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
    # broadcast.send("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))

def publish_readings():
    pass