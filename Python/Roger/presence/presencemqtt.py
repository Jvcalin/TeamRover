if __name__ == '__main__':
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent))  # Make common library available

import common.mqttService as mqtt

class PresenceMqtt:

    def __init__(self, parent):
        # initialize mqtt
        mqttSubs = [mqtt.RoverMqttSubscription("roger/sensors/feather", lambda x: self.getFeatherSensors(x)),
                    mqtt.RoverMqttSubscription("roger/sensors/matrix", lambda x: self.getMatrixSensors(x)),
                    mqtt.RoverMqttSubscription("roger/cmd/presence", lambda x: self.getPresenceCmd(x))]
        self.mqtt = mqtt.RoverMqtt("Roger_Presence_Loop", mqttSubs)
        self.eventbasetopic = "roger/events"
        self.structuresbasetopic = "roger/structures/proxarray"
        self.parent = parent

    def getFeatherSensors(self, payload):
        # get the values from the prox sensors
        # and call feelProx with tuple
        pass

    def getMatrixSensors(self, payload):
        # get the values from the imu
        # and call reorient and feelRotate
        pass

    def getPresenceCmd(self, payload):
        # roger/cmd/presence/prox
        if payload == "prox":
            self.mqtt.publishArray()

    def publishEvent(self, eventname, content):
        mqtt.publish(self.eventbasetopic + '/' + eventname, content)

    def publishArray(self):
        # for now we send the array oriented to mag north, but later we may use orientation
        mqtt.publish(self.structuresbasetopic, self.prox.array.GetArray(0))


