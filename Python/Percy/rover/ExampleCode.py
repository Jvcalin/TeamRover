

"""
SERVOS
"""

import time
from adafruit_crickit import crickit

print("1 Servo demo!")

while True:
    print("Moving servo #1")
    crickit.servo_1.angle = 0      # right
    time.sleep(1)
    crickit.servo_1.angle = 90     # middle
    time.sleep(1)
    crickit.servo_1.angle = 180    # left
    time.sleep(1)
    crickit.servo_1.angle = 90     # middle
    time.sleep(1)
    # and repeat!

print("4 Servo demo!")

# make a list of all the servos
servos = (crickit.servo_1, crickit.servo_2, crickit.servo_3, crickit.servo_4)

while True:
    # Repeat for all 4 servos
    for my_servo in servos:
        # Do the wave!
        print("Moving servo #", servos.index(my_servo)+1)
        my_servo.angle = 0      # right
        time.sleep(0.25)
        my_servo.angle = 90     # middle
        time.sleep(0.25)
        my_servo.angle = 180    # left
        time.sleep(0.25)
        my_servo.angle = 90     # middle
        time.sleep(0.25)
        my_servo.angle = 0      # right

import time
from adafruit_crickit import crickit

print("1 Servo demo with custom pulse widths!")

crickit.servo_1.set_pulse_width_range(min_pulse=500, max_pulse=2500)

while True:
    print("Moving servo #1")
    crickit.servo_1.angle = 0      # right
    time.sleep(1)
    crickit.servo_1.angle = 180    # left
    time.sleep(1)


"""
MOTORS
"""

import time
from adafruit_crickit import crickit

print("Dual motor demo!")

# make two variables for the motors to make code shorter to type
motor_1 = crickit.dc_motor_1
motor_2 = crickit.dc_motor_2

while True:
    motor_1.throttle = 1  # full speed forward
    motor_2.throttle = -1 # full speed backward
    time.sleep(1)

    motor_1.throttle = 0.5  # half speed forward
    motor_2.throttle = -0.5 # half speed backward
    time.sleep(1)

    motor_1.throttle = 0  # stopped
    motor_2.throttle = 0  # also stopped
    time.sleep(1)

    motor_1.throttle = -0.5  # half speed backward
    motor_2.throttle = 0.5   # half speed forward
    time.sleep(1)

    motor_1.throttle = -1  # full speed backward
    motor_2.throttle = 1   # full speed forward
    time.sleep(1)

    motor_1.throttle = 0  # stopped
    motor_2.throttle = 0  # also stopped
    time.sleep(0.5)

    # and repeat!


"""
TOF, APDS SENSORS
"""
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.
import time

import board
import busio

import adafruit_vl53l0x

# Initialize I2C bus and sensor.
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
while True:
    print("Range: {0}mm".format(vl53.range))
    time.sleep(1.0)


import time
import board
from adafruit_apds9960.apds9960 import APDS9960

i2c = board.I2C()
apds = APDS9960(i2c)

apds.enable_proximity = True

while True:
    print(apds.proximity)
    time.sleep(0.2)




"""
ACCELEROMETER
"""
import time
import board
import adafruit_pct2075

i2c = board.I2C()  # uses board.SCL and board.SDA
pct = adafruit_pct2075.PCT2075(i2c)

while True:
    print("Temperature: %.2f C" % pct.temperature)
    time.sleep(0.5)


# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = LSM6DSOX(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
    print("")
    time.sleep(0.5)


# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display magnetometer data once per second """

import time
import board
import adafruit_lis3mdl

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_lis3mdl.LIS3MDL(i2c)

while True:
    mag_x, mag_y, mag_z = sensor.magnetic

    print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))
    print("")
    time.sleep(1.0)

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display compass heading data five times per second """
import time
from math import atan2, degrees
import board
import adafruit_lis3mdl

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_lis3mdl.LIS3MDL(i2c)


def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle


def get_heading(_sensor):
    magnet_x, magnet_y, _ = _sensor.magnetic
    return vector_2_degrees(magnet_x, magnet_y)


while True:
    print("heading: {:.2f} degrees".format(get_heading(sensor)))
    time.sleep(0.2)


# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS

# To use LSM6DS33, comment out the LSM6DSOX import line
# and uncomment the next line
# from adafruit_lsm6ds.lsm6ds33 import LSM6DS33 as LSM6DS

# To use ISM330DHCX, comment out the LSM6DSOX import line
# and uncomment the next line
# from adafruit_lsm6ds.lsm330dhcx import ISM330DHCX as LSM6DS

from adafruit_lis3mdl import LIS3MDL

i2c = board.I2C()  # uses board.SCL and board.SDA
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

while True:
    acceleration = accel_gyro.acceleration
    gyro = accel_gyro.gyro
    magnetic = mag.magnetic
    print(
        "Acceleration: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} m/s^2".format(*acceleration)
    )
    print("Gyro          X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} rad/s".format(*gyro))
    print("Magnetic      X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} uT".format(*magnetic))
    print("")
    time.sleep(0.5)



"""
OLED
"""
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, and some white text.
"""

import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(128, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(118, 24, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
splash.append(text_area)

while True:
    pass
