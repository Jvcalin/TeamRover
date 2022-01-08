import wifimqtt as mqtt

"""
def initialize(oled, mqtt):
    myOled = oled
    myMqtt = mqtt
"""

def send(message):
    print(str(message))
    if mqtt.MQTT:
        mqtt.publishMessage(str(message))

