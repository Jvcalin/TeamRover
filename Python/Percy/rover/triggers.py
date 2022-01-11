import motors
import proximity
import sensors


def tick():
    #front proximity trigger (the higher the number the farther it is)
    if proximity.get_value() < 150:
        print("Front proximity trigger!!!")
        if motors.is_moving_forward():
            motors.stop()

    #rear proximity trigger  (the higher the number the closer it is)
    if sensors.get_rear_proximity() > 5:
        print("Rear proximity trigger!!!")
        if motors.is_moving_backward():
            motors.stop()
