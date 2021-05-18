import time
from adafruit_crickit import crickit

print("Dual motor demo!")

# make two variables for the motors to make code shorter to type
left_motor = crickit.dc_motor_1
right_motor = crickit.dc_motor_2

while True:
    left_motor.throttle = 1   # full speed forward
    right_motor.throttle = 1  # full speed backward
    time.sleep(2)

    left_motor.throttle = 0.5   # half speed forward
    right_motor.throttle = 0.5  # half speed backward
    time.sleep(1)

    left_motor.throttle = 0  # stopped
    right_motor.throttle = 0  # also stopped
    time.sleep(1)

    left_motor.throttle = -0.5  # half speed backward
    right_motor.throttle = -0.5   # half speed forward
    time.sleep(1)

    left_motor.throttle = -1  # full speed backward
    right_motor.throttle = -1   # full speed forward
    time.sleep(1)

    left_motor.throttle = 0  # stopped
    right_motor.throttle = 0  # also stopped
    time.sleep(0.5)



    # and repeat!
