import time
import broadcast
# import wifimqtt as mqtt
import motors
import WiFi

# import servos
import sensors
# import motion
import triggers

# Setup
# mqtt.initialize("Percy", motors.mqttReceiveCommand)
# WiFi.initialize(motors.receive_command)

broadcast.send("Setup complete.")
# mqtt.publishMessage("roger/status/feather", "Susan has connected to Roger")


def quickLoop():
    motors.tick()
    sensors.tick()
    triggers.tick()
    # pass


def slowLoop():
    # mqtt.checkMessages()
    WiFi.tick()
    # pass

def to_seconds(nanoseconds):
    return nanoseconds/nanosecsPerSec


# Main Loop
# Each loop iteration is 1 second
# The internal loop is 50 cycles
nanosecsPerSec = 1000000000
cyclesPerSecond = 50
cycleTime_ns = nanosecsPerSec/cyclesPerSecond
counter = 0
ctr2 = 0
broadcast.send("Starting Loop...")
"""
while True:
    t = time.monotonic_ns()
    for i in range(cyclesPerSecond):
        quickLoop()
    counter += 1
    slowLoop()
    tt = time.monotonic_ns() - t
    if nanosecsPerSec > tt:
        time.sleep(to_seconds(nanosecsPerSec - tt))
    broadcast.send(f"{counter}: {to_seconds(time.monotonic_ns() - t):.2f} sec -> {to_seconds(tt):.2f} sec")
"""

while True:
    t = time.monotonic_ns()
    ctr2 += 1
    slowLoop()
    while (time.monotonic_ns() - t) < nanosecsPerSec:
        quickLoop()
        counter += 1
    broadcast.send(f"{ctr2}: {to_seconds(time.monotonic_ns() - t):.2f} sec -> {counter} iterations")
    counter = 0




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