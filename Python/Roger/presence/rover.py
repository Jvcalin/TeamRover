import presence.proximity as Prox
import presence.grid as Grid
import common.mycollections as Coll
import presence.matrixcreator as Matrix
import presence.featherhuzzah as Feather


class Rover:
    
    def __init__(self):
        self.currentPos = (0,0) #x,y
        self.prox = Prox.ProximityArray()  #each point in array is a distance measured by the sensors
        self.space = Grid.Space2D()  #the map on which the rover is travelling
        self.proxsensors = { "front":Matrix.ProxSensor(0), 
                            "left":Matrix.ProxSensor(45), 
                            "right":Matrix.ProxSensor(-45), 
                            "back":Matrix.ProxSensor(180)}
        self.motion = Matrix.Motion(self)
        self.leds = Matrix.LEDArray()
        self.motion.readSensors()
        self.prox.orientation = self.motion.getOrientationAngle  #the way the rover is facing in relation to mag north 0 (degrees)
        self.events = {}

    def readSensors(self):
        for s in self.proxsensors:
            d = s.read()
            self.prox.register(s.angle, v)
            self.space.addVector(self.currentPos, self.prox.orientation + s.angle, d)
        self.motion.read()
        self.leds.applyProxArray(self.prox.GetArray(self.prox.orientation))


    def checkEvents(self):
        for e in self.events:
            if e.check():
                e.trigger()


class RoverEvent:
        def __init__(self, checkEvent, triggerEvent):
            self.checkF = checkEvent
            self.triggerF = triggerEvent

        def check(self):
            return self.checkF()

        def trigger(self):
            self.triggerF()



