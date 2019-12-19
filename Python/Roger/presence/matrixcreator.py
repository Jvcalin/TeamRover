from matrix_lite import led, sensors
import time
import statistics as stat
from math import pi, sin


class Motion:

    def __init__(self,parent):
        self.parent = parent
        self.xAccel = Coll.RollingArray(25)  
        self.yAccel = Coll.RollingArray(25)  
        self.zAccel = Coll.RollingArray(25)  
        self.xSpin = Coll.RollingArray(25)
        self.ySpin = Coll.RollingArray(25)
        self.zSpin = Coll.RollingArray(25)
        self.tilt = Coll.RollingArray(25)
        self.roll = Coll.RollingArray(25)
        self.yaw = Coll.RollingArray(25)

    def read(self):
        imu = sensors.imu.read()
        self.xAccel.push(imu.accel_x)  
        self.yAccel.push(imu.accel_y)
        self.zAccel.push(imu.accel_z)
        self.xSpin.push(imu.gyro_x)  
        self.xSpin.push(imu.gyro_y)  
        self.xSpin.push(imu.gyro_z)  
        self.tilt.push(imu.tilt)  
        self.roll.push(imu.roll)  
        self.yaw.push(imu.yaw)  
        #TODO: finish

    def getOrientationAngle(self):
        return self.yaw / 2 * pi * 360  #TODO: calculate angle from here


class LEDArray:
    MAXDISTANCE = 360

    def __init__(self):
        self.ledarray = []
        for i in range(35):
            self.ledarray.append({'r':0, 'g':0, 'b':0, 'w':0})


    def applyProxArray(self, array):
        ratio = len(array) / len(self.ledarray)
        for i in range(0,len(self.ledarray)):
            low = round(i * ratio)
            high = round((i + 1) * ratio)
            if high > len(array):
                high = len(array)
            subarray = []
            for x in array[low:high]:
                subarray.append(x.getValue())
            intensity = round(stat.mean(subarray) / MAXDISTANCE * 255)
            self.ledarray[i] = {'r':intensity, 'g':0, 'b':0, 'w':0}  #red
        led.set(self.ledarray)

    def applyColor(self, color):
        led.set(color)

    def clear(self):
        led.set()

    def applyRoundinaCircle(self, times, color):
        everloop = ['black'] * led.length
        everloop[0] = color
        for i in range(times):
            everloop.append(everloop.pop(0))
            led.set(everloop)
            time.sleep(0.050)
        clear()

    def applyRainbow(self, times):
        everloop = ['black'] * led.length

        ledAdjust = 0.51 # MATRIX Creator

        frequency = 0.375
        counter = 0.0
        tick = len(everloop) - 1

        for i in range(times):
        # Create rainbow
            for i in range(len(everloop)):
                r = round(max(0, (sin(frequency*counter+(pi/180*240))*155+100)/10))
                g = round(max(0, (sin(frequency*counter+(pi/180*120))*155+100)/10))
                b = round(max(0, (sin(frequency*counter)*155+100)/10))

                counter += ledAdjust

                everloop[i] = {'r':r, 'g':g, 'b':b}

            # Slowly show rainbow
            if tick != 0:
                for i in reversed(range(tick)):
                    everloop[i] = {}
                tick -= 1

            led.set(everloop)

            sleep(.035)

        clear()

