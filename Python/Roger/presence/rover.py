import proximity as Prox
import grid as Grid
import matrixcreator as Matrix
import featherhuzzah as Feather
from common import events as Events
from common import mycollections as Coll

class Rover:
    
    def __init__(self):
        self.currentPos = (0,0) #x,y
        self.prox = Prox.ProximityArray()  #each point in array is a distance measured by the sensors
        self.space = Grid.Space2D()  #the map on which the rover is travelling
        self.proxsensors = Feather.ProxSensors
        self.motion = Matrix.Motion(self)
        self.leds = Matrix.LEDArray()
        self.motion.readSensors()
        self.prox.orientation = self.motion.getOrientationAngle  #the way the rover is facing in relation to mag north 0 (degrees)
        self.did = Events.Did()
        self.sense = Events.Sense()
        self.events = {
            "forward": RogerEvent(self.did.goforward, self.sense.Forward),
            "spinleft": RogerEvent(self.did.spinleft, self.sense.spinleft),
            "spinright": RogerEvent(self.did.spinright, self.sense.spinleft),
            "backward": RogerEvent(self.did.gobackward, self.sense.Backward),
            "tipforward": RogerEvent(self.did.tipforward, self.sense.tipforward),
            "tipback": RogerEvent(self.did.TipBack, self.sense.TipBack),
            "tipleft": RogerEvent(self.did.tipleft, self.sense.tipleft),
            "tipright": RogerEvent(self.did.tipright, self.sense.Right),
            "brake": RogerEvent(self.did.brake, self.sense.brake),
            "bump": RogerEvent(self.did.bump, self.sense.bump)
            }

    def readSensors(self):
        for s in self.proxsensors:
            d = s.read()
            self.prox.register(s.angle, v)
            self.space.addVector(self.currentPos, self.prox.orientation + s.angle, d)
        self.motion.read()
        self.leds.applyProxArray(self.prox.GetArray(self.prox.orientation))


    def checkEvents(self):
        for e in self.events:
            if self.events[e].check():
                self.events[e].trigger()


class RoverEvent(Events.EventNotifier):
        def __init__(self, checkEvent, triggerEvent):
            self.checkF = checkEvent
            self.triggerF = triggerEvent
            Events.EventNotifier.__init__(self)

        def check(self):
            return self.checkF()

        def trigger(self):
            self.notify("1")
            self.triggerF()



