if __name__ == '__main__':
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent))  #Make common library available
    # sys.path.append(str(Path(__file__)))

import common.mqttService as mqtt
import proximity as prox

class Presence:
    
    def __init__(self):
        self.stop = False
        #initialize mqtt
        mqttSubs = [mqtt.RoverMqttSubscription("roger/sensors/feather", lambda x : self.getFeatherSensors(x)), 
                    mqtt.RoverMqttSubscription("roger/sensors/matrix", lambda x : self.getMatrixSensors(x)), 
                    mqtt.RoverMqttSubscription("roger/events/feather", lambda x : self.getFeatherEvent(x))] 
        self.mqtt = mqtt.RoverMqtt("Roger_Presence_Loop", mqttSubs)

        self.prox = prox.ProximityArray()

    def __del__(self):
        pass

    def tick(self):      
        return self.stop

    def getFeatherSensors(self, payload):
        pass

    def getMatrixSensors(self, payload):
        pass
    
    def getFeatherEvent(self, payload):
        pass

    def getMatrixEvent(self, payload):
        pass

    
