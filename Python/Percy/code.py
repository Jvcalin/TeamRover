import time
import broadcast
import wifimqtt as mqtt
import motors

# import servos
import sensors
# import motion

# Setup
mqtt.initialize("Percy", motors.mqttReceiveCommand)

broadcast.send("Setup complete.")
# mqtt.publishMessage("roger/status/feather", "Susan has connected to Roger")


def quickLoop():
    motors.tick()
    sensors.tick()


def slowLoop():
    mqtt.checkMessages()


# Main Loop
# Each loop iteration is 1 second
# The internal loop is 60 cycles
cyclesPerSecond = 60
cycleTime_ns = 1000000000/cyclesPerSecond
counter = 0
broadcast.send("Starting Loop...")
while True:
    t1 = time.monotonic_ns()
    for i in range(cyclesPerSecond):
        t = time.monotonic_ns()
        quickLoop()
        tt = time.monotonic_ns() - t
        if cycleTime_ns > tt:
            time.sleep((cycleTime_ns - tt)/1000000000)
    counter += 1
    slowLoop()
    broadcast.send("{}: {:.2f} sec".format(counter, (time.monotonic_ns() - t1)/1000000000))

"""
import time

import board
import busio

import adafruit_vl53l0x
import broadcast

print ("Starting I2C")
# Initialize I2C bus and sensor.
#  = busio.I2C(board.SCL, board.SDA)
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

print("I2C set up")

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

"""