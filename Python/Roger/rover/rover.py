#sys.path.append("C:\Users\jvcal\Google Drive\IoT_Boards\TeamRover")
#from ...rogercommon import mqttService as mqtt
#from ...Python import Roger
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))  #Make common library available
#sys.path.append(str(Path(__file__)))

import common.mqttService as mqtt
import common.triggers as triggers
import common.shapes as shapes
# import proximity as Prox
# import grid as Grid
import matrixcreator as matrix # import Motion, LEDArray, Sensors, Microphones
# import featherhuzzah as Feather
# from ...common import triggers as trig
import common.rovercollections as Coll
import json
import os

class Rover:
    
    def __init__(self):
        self.stop = False
        #initialize mqtt
        mqttSubs = [mqtt.RoverMqttSubscription("roger/cmd/matrix/led", lambda x : self.LEDCmd(x)), 
                    mqtt.RoverMqttSubscription("roger/cmd/matrix/triggers/add", lambda x : self.AddTriggerCmd(x)), 
                    mqtt.RoverMqttSubscription("roger/cmd/matrix", lambda x : self.MatrixCmd(x))] 
        self.mqtt = mqtt.RoverMqtt("Roger_Rover_Loop", mqttSubs)

        self.motion = matrix.Motion()
        self.leds = matrix.LEDArray()
        self.timers = [50,2500]   #initial values - they count to 0
        self.timerSizes = [50,2500]  #size of timer

        #self.motion.readSensors()

        #set up the trigger manager
        self.triggerFile = "../triggers.txt"
        self.triggerFileSize = os.path.getsize(self.triggerFile)
        self.BuildTriggers()

    def __del__(self):
        self.SaveTriggers()

    def tick(self):
        self.motion.read()

        if self.checkTimer(0):
            self.motion.publishSensors(self.mqtt)

        if self.checkTimer(1):
            self.triggers.check()
       
        return self.stop

    def checkTimer(self, index):
        if self.timers[index] <= 0:
            self.timers[index] = self.timerSizes[index]
            return True
        else:
            self.timers[index] -= 1
            return False

    def LEDCmd(self, cmdText):
        print("LEDCmd Received " + cmdText)
        self.leds.parseCommand(cmdText)

    def AddTriggerCmd(self, cmdText):
        print("AddTriggerCmd Received " + cmdText)
        topic = "roger/event/matrix/"
        t = json.loads(cmdText)
        sections = []
        for s in t["shape"]:
            ss = shapes.GraphSection(s["size"],s["slope"],s["average"],s["error"])
            sections.append(ss)
        shape = shapes.GraphShape(sections)
        tt = triggers.ArrayTrigger(t["name"],
            t["sensor"], 
            self.motion.sensors[t["sensor"]], 
            shape,
            lambda : self.PublishEvent(topic + t["name"],self.motion.sensors[t["sensor"]].getAvg()))
        self.triggers.add(tt)
        self.SaveTriggers()

    def MatrixCmd(self, cmdText):
        print("MatrixCmd Received " + cmdText)
        if (cmdText == "stop"):
            self.stop = True

    def PublishEvent(self, topic, message):
        mqtt.publish(topic, message)

    def BuildTriggers(self):
        self.triggers = triggers.TriggerCollection()
        for t in self.CreateTriggers():
            self.triggers.add(t)

        # #add an additional trigger to reload the triggers if the file changes
        # fileChangeTrigger = triggers.Trigger(self.triggerFileSize,
        # lambda x : x != os.path.getsize(self.triggerFile),
        # self.BuildTriggers)
        # self.triggers.add(fileChangeTrigger)

    def CreateTriggers(self):
        topic = "roger/event/matrix/"
        self.triggerFileSize = os.path.getsize(self.triggerFile)
        f = open(self.triggerFile, "rt")
        arrayTriggerRecords = json.loads(f.read())
        f.close()
        triggerlist = []
        for t in arrayTriggerRecords:
            sections = []
            for s in t["shape"]:
                ss = shapes.GraphSection(s["size"],s["slope"],s["average"],s["error"])
                sections.append(ss)
            shape = shapes.GraphShape(sections)
            tt = triggers.ArrayTrigger(t["name"],
                t["sensor"], 
                self.motion.sensors[t["sensor"]], 
                shape,
                lambda : self.PublishEvent(topic + t["name"],self.motion.sensors[t["sensor"]].getAvg()))
            triggerlist.append(tt)
        return triggerlist

    def SaveTriggers(self):
        arrayTriggerRecords = []
        for t in self.triggers.triggers:
            sections = []
            for s in t.shape.sections:
                sections.append({"size":s.size, "slope":s.slope, "average":s.average, "error":s.error})
            arrayTriggerRecords.append({"name":t.name,"sensor":t.sensor,"shape":sections})
        f = open(self.triggerFile, "wt")
        f.write(json.dumps(arrayTriggerRecords))
        f.close()


# r = Rover()
# r.SaveTriggers()




    #    #go forward
    #     triggerlist.append(triggers.Trigger(self.motion.sensors["xAccel"],
    #                        lambda x : x.getTrend(10) > 0,
    #                        lambda : self.PublishEvent(topic + "forward", self.motion.sensors["xAccel"].getTrend(10))))

        # self.currentPos = (0,0) #x,y
        # self.prox = Prox.ProximityArray()  #each point in array is a distance measured by the sensors
        # self.space = Grid.Space2D()  #the map on which the rover is travelling
        # self.proxsensors = Feather.ProxSensors
        # self.prox.orientation = self.motion.getOrientationAngle  #the way the rover is facing in relation to mag north 0 (degrees)
        # self.did = Events.Did()
        # self.sense = Events.Sense()
        # self.events = {
        #     "forward": RogerEvent(self.did.goforward, self.sense.Forward),
        #     "spinleft": RogerEvent(self.did.spinleft, self.sense.spinleft),
        #     "spinright": RogerEvent(self.did.spinright, self.sense.spinleft),
        #     "backward": RogerEvent(self.did.gobackward, self.sense.Backward),
        #     "tipforward": RogerEvent(self.did.tipforward, self.sense.tipforward),
        #     "tipback": RogerEvent(self.did.TipBack, self.sense.TipBack),
        #     "tipleft": RogerEvent(self.did.tipleft, self.sense.tipleft),
        #     "tipright": RogerEvent(self.did.tipright, self.sense.Right),
        #     "brake": RogerEvent(self.did.brake, self.sense.brake),
        #     "bump": RogerEvent(self.did.bump, self.sense.bump)
        #     }

    # def readSensors(self):
    #     for s in self.proxsensors:
    #         d = s.read()
    #         self.prox.register(s.angle, v)
    #         self.space.addVector(self.currentPos, self.prox.orientation + s.angle, d)
    #     self.motion.read()
    #     self.leds.applyProxArray(self.prox.GetArray(self.prox.orientation))


    # def checkEvents(self):
    #     for e in self.events:
    #         if self.events[e].check():
    #             self.events[e].trigger()


# class RoverEvent(Events.EventNotifier):
#         def __init__(self, checkEvent, triggerEvent):
#             self.checkF = checkEvent
#             self.triggerF = triggerEvent
#             Events.EventNotifier.__init__(self)

#         def check(self):
#             return self.checkF()

#         def trigger(self):
#             self.notify("1")
#             self.triggerF()



