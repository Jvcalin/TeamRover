if __name__ == '__main__':
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent))  # Make common library available

from matrix_lite import led, sensors
# from common import rovercollections as collections
from common import eventmonitor as ev
import time
import statistics as stat
from math import pi, sin
import json


class Motion:

    def __init__(self, mqtt):
        arraysize = 300
        self.rover = "roger"
        self.sensors = {"accel": ev.EventMonitorTuple(self.rover, "accelerometer", arraysize)}
                        # , "spin": ev.EventMonitor(self.rover, "spin", arraysize)
                        # , "mag": ev.EventMonitor(self.rover, "magnetometer", arraysize)
                        # , "direction": ev.EventMonitor(self.rover, "direction", arraysize)
                        # , "orientation": ev.EventMonitor(self.rover, "orientation", arraysize)}
        self.sensors["accel"].onEventOccur = lambda x: self.publishEvent("accelerometer", x)
        # self.sensors["spin"].onEventOccur = lambda x: self.publishEvent("spin", x)
        # self.sensors["mag"].onEventOccur = lambda x: self.publishEvent("magnetometer", x)
        # self.sensors["direction"].onEventOccur = lambda x: self.publishEvent("direction", x)
        # self.sensors["orientation"].onEventOccur = lambda x: self.publishEvent("orientation", x)
        self.mqtt = mqtt
        # self.read()

    def read(self):
        imu = sensors.imu.read()
        self.sensors["accel"].post((float(imu.accel_x), float(imu.accel_y), float(imu.accel_z)))
        # self.sensors["spin"].post((float(imu.gyro_x), float(imu.gyro_y), float(imu.gyro_z)))
        # self.sensors["mag"].post((float(imu.mag_x), float(imu.mag_y), float(imu.mag_z)))
        # self.sensors["direction"].post((float(imu.pitch), float(imu.roll), float(imu.yaw)))
        # self.sensors["orientation"].post(self.getOrientationAngle(imu.yaw))
        # print([imu.accel_x, imu.accel_y, imu.accel_z, imu.gyro_x, imu.gyro_y, imu.mag_z, imu.pitch, imu.roll, imu.yaw])

    def getOrientationAngle(self, val):
        return val  # * 180 / pi

    def publishEvent(self, name, payload):
        content = json.dumps(payload)
        self.mqtt.publish("roger/sensors/matrix/imu/" + name, content)

    def startLogging(self, sensorname="ALL"):
        if sensorname == "ALL":
            for s in self.sensors.keys():
                self.sensors[s].startLog()
        else:
            self.sensors[sensorname].startLog()

    def stopLogging(self, sensorname="ALL"):
        if sensorname == "ALL":
            for s in self.sensors.keys():
                self.sensors[s].stopLog()
        else:
            self.sensors[sensorname].stopLog()

    # def serializeSensors(self):
    #     sensorsDict = {}
    #     for s in self.sensors:
    #         sensorsDict[s] = self.sensors[s].getAvg()
    #     return sensorsDict


class LEDArray:
    MAXDISTANCE = 360

    def __init__(self):
        self.ledarray = []
        for i in range(led.length):
            self.ledarray.append({'r': 0, 'g': 0, 'b': 0, 'w': 0})

    def parseCommand(self, payload):
        print("Parsing " + payload)
        arguments = payload.split(",")
        method = "apply" + arguments.pop(0)
        print("Parsed: " + method)
        print(arguments)
        command = getattr(self, method)
        command(self.ledarray, arguments)
        
    def applyProxArray(self, array):  # array is an array of integers
        ratio = len(array) / len(self.ledarray)
        for i in range(0, len(self.ledarray)):
            low = round(i * ratio)
            high = round((i + 1) * ratio)
            if high > len(array):
                high = len(array)
            intensity = round(stat.mean(array[low:high]) / self.MAXDISTANCE * 255)
            self.ledarray[i] = {'r': intensity, 'g': 0, 'b': 0, 'w': 0}  # red
        led.set(self.ledarray)

    def applyColor(self, ledarray, color):
        print("Applying color " + color[0])
        led.set(color[0])

    def applyClear(self, ledarray, nothing):
        led.set()

    def applyRoundinaCircle(self, ledarray, args):
        everloop = ['black'] * led.length
        everloop[0] = 'blue' #args[0]
        for i in range(int(args[0]) * led.length):
            everloop.append(everloop.pop(0))
            led.set(everloop)
            time.sleep(0.050)
        self.applyClear(ledarray,1)

    def applyRainbow(self, ledarray, times):
        print("Applying rainbow")
        
        everloop = ['black'] * led.length

        ledAdjust = 0.51 # MATRIX Creator

        frequency = 0.375
        counter = 0.0
        tick = len(everloop) - 1

        for j in range(int(times[0]) * len(everloop)):
        # Create rainbow
            for i in range(len(everloop)):
                r = round(max(0, (sin(frequency*counter+(pi/180*240))*155+100)/10))
                g = round(max(0, (sin(frequency*counter+(pi/180*120))*155+100)/10))
                b = round(max(0, (sin(frequency*counter)*155+100)/10))

                counter += ledAdjust

                everloop[i] = {'r': r, 'g': g, 'b': b}

            # Slowly show rainbow
            if tick != 0:
                for i in reversed(range(tick)):
                    everloop[i] = {}
                tick -= 1

            led.set(everloop)

            time.sleep(.035)

        self.applyClear(ledarray,1)





class Sensors:
    def __init__(self):
        pass
        #temp/pressure/hum
        #uv

class Microphones:
    def __init__(self):
        pass
        #record sound
        #sound direction


