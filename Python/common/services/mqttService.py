import paho.mqtt.client as mqtt

rogerMqtt = mqtt.Client("RogerMQTT_Pi", False)  # clean sessions =false so subsriptions are maintained and messages are saved if disconnected


def initializemqtt(rover):
    theRover = rover
    rogerMqtt.on_message = on_message
    rogerMqtt.on_connect = on_connect
    rogerMqtt.connect("192.168.1.25", 1883)
    rogerMqtt.subscribe("roger/cmd/#", 2)
    rogerMqtt.subscribe("roger/sensors/#", 2)
    rogerMqtt.loop_start()
    rogerMqtt.publish("roger/status", "presence loop starting", 2, True)


def closemqtt():
    rogerMqtt.publish("roger/status", "presence loop stopping", 2, True)
    rogerMqtt.loop_stop()


def on_message(client, userdata, message):
    print("got message")
    print(client)
    print(userdata)
    print(message.payload.decode("utf-8"))
    print(message.topic)
    print(message.retain)
    print(message.qos)


# TODO do something with the message
# if cmd, call to execute cmd
# if sensor, update state vars for device

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# client.subscribe("roger/cmd/#", 2)
# client.subscribe("roger/sensors/#", 2)

def getroute(path):
    # routes is robotname/messagetype/device/item/subitem
    route = path.split("/")
    return route
