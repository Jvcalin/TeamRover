"""
The Trigger Collection class is a collection of triggers.
Add and Trigger objects
Call check() to cycle through the triggers and run if triggered
Call setAll() to re-set all triggers
"""
class TriggerCollection:

    def __init__(self):
        self.triggers = []

    def add(self, f):
        self.triggers.append(f)

    def remove(self, f):
        self.triggers.remove(f)

    def check(self):
        for f in self.triggers:
            if (f.check()):
                f.doFunction()

    def setAll(self):
        for f in self.triggers:
            f.setTrigger()

"""
A trigger has:
A reference to the object to observe
A lambda function that returns true or false -- true means the trigger is triggered, false is not
 -- the lambda function must accept the obj to observe:  lambda x : x > 10
A function that will do the thing if the trigger is triggered
If runOnce is set to true, the Trigger will only run once.  It will only run again when "setTrigger" is called
"""
class Trigger:

    def __init__(self, objToObserve, willTriggerIfFunction, doWhenTriggered):
        self.obj = objToObserve
        self.checkFunction = willTriggerIfFunction
        self.doFunction = doWhenTriggered
        self.isSet = True
        self.runOnce = False

    def check(self):
        if self.isSet and self.checkFunction(self.obj):
            if self.runOnce:
                self.isSet = False
            return True
        else:
            return False
    
    def setTrigger(self):
        self.isSet = True

class ArrayTrigger:
    def __init__(self, name, sensor, arrayToObserve, shapeToMatch, doWhenMatched):
        self.name = name
        self.sensor = sensor
        self.array = arrayToObserve
        self.shape = shapeToMatch
        self.doFunction = doWhenMatched
        self.isSet = True
        self.runOnce = False

    def check(self):
        if self.isSet and self.shape.compare(self.array.get()):
            if self.runOnce:
                self.isSet = False
            return True
        else:
            return False
    
    def setTrigger(self):
        self.isSet = True

class ArrayTriggerRecord:
    def __init__(self, topicName, sensorName, shape):
        self.name = topicName
        self.sensor = sensorName
        self.shape = shape

"""

class SampleObj:
    def __init__(self, val1, val2):
        self.value1 = val1
        self.value2 = val2

    def dosomething(self):
        self.value1 += 1
        self.value2 *= 2

def PrintMe(message):
    print(message)


obj = SampleObj(23,45)
# cfunc = lambda x,y : x.value1 > y["max"]

trig1 = Trigger(obj, lambda x,y : x.value1 > y["max"], {"max":25}, lambda : PrintMe("trig1 triggered"))
trig2 = Trigger(obj, lambda x,y : x.value2 > y["max"] or x.value1 == y["equals"], {"max":34, "equals":360}, lambda : PrintMe("trig2 triggered")  )

# while not trig.check():
#   obj.dosomething()

# print(obj.value1, " ", obj.value2)

trigs = TriggerCollection()
trigs.add(trig1)
trigs.add(trig2)


for i in range(25):
    obj.dosomething()
    print(obj.value1, " ", obj.value2)
    trigs.check()

"""
# eventually, we would like the executive
# to be able to create events and link a reaction to them

# Context is a set of events that can be loaded or unloaded
#  

"""
# what to do when an event occurs
class Sense:
    def forward(self):
        pass

    def backward(self):
        pass

    def spinleft(self):
        pass

    def spinright(self):
        pass

    def tipforward(self):
        pass

    def tipbackward(self):
        pass

    def tipleft(self):
        pass

    def tipright(self):
        pass

    def brake(self):
        pass

    def bump(self):
        pass


# check if an event occurred
class Did:
    def goforward(self):
        pass

    def gobackward(self):
        pass

    def spinleft(self):
        pass

    def spinright(self):
        pass

    def tipforward(self):
        pass

    def tipbackward(self):
        pass

    def tipleft(self):
        pass

    def tipright(self):
        pass

    def brake(self):
        pass

    def bump(self):
        pass









def watch(value):
    print(value)

e = EventNotifier()
e.subscribe(watch)
e.notify("aaa")
"""