if __name__ == '__main__':
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent))  # Make common library available
    # sys.path.append(str(Path(__file__)))


import proximity as prox
import presencemqtt as mqtt


class Presence:

    def __init__(self):
        self.stop = False
        self.prox = prox.ProximityArray()
        self.mqtt = mqtt.PresenceMqtt(self)
        self.timers = [50, 2500]  # initial values - they count to 0
        self.timerSizes = [50, 2500]  # size of timer

    def __del__(self):
        pass

    def tick(self):
        return self.stop

    def feelProx(self, sensors):
        # Sensor order: Front, Left, Right, Back
        self.prox.sense(0, sensors[0])
        self.prox.sense(315, sensors[1])
        self.prox.sense(45, sensors[2])
        self.prox.sense(180, sensors[3])

    def feelRotate(self, value):
        # value should be calibrated to translate into angle
        # this calibration should be refined over time
        angle = value * 1
        self.prox.rotate(angle)  # this comes from sensing gyro

    def reorient(self, angle):
        self.prox.orientation = angle  # this comes from sensing magnetic north



