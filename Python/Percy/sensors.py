import time
import board
import broadcast
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import adafruit_vl53l0x
from adafruit_apds9960.apds9960 import APDS9960

i2c = board.I2C()
apds = APDS9960(i2c)

apds.enable_proximity = True

"""
import time

import board
import busio


import broadcast

# Initialize I2C bus and sensor.
#  = busio.I2C(board.SCL, board.SDA)
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

# Main loop will read the range and print it every second.
# while True:
#     print("Range: {0}mm".format(vl53.range))
#     time.sleep(1.0)

def tick():
    broadcast.send("Range: {0}mm".format(vl53.range))

"""



print("Initializing accelerometer")
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = LSM6DSOX(i2c)
print("Accelerometer ready")

vl53 = adafruit_vl53l0x.VL53L0X(i2c)
print("Time of flight sensor ready")

apds = APDS9960(i2c)

apds.enable_proximity = True

def tick():
    broadcast.send("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
    # broadcast.send("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
    # broadcast.send("Range: {0}mm".format(vl53.range))
    # broadcast.send("Proximity: {0}".format(apds.proximity))
    # broadcast.send(int(apds.proximity))
    #broadcast.send("")
    #time.sleep(0.5)

